"""Functions for registering environments using public functions ``make``, ``register`` and ``spec``."""

from __future__ import annotations

import contextlib
import copy
import dataclasses
import difflib
import importlib
import importlib.util
import json
import re

from dataclasses import dataclass, field
from enum import Enum
from types import ModuleType
from typing import Any, Iterable

from maspy.learning.core import Model
#from maspy.learning.vector import VectorEnv 
import maspy.learning.wrappers as wrappers


import importlib.metadata as metadata
from typing import Protocol


MODEL_ID_RE = re.compile(
    r"^(?:(?P<namespace>[\w:-]+)\/)?(?:(?P<name>[\w:.-]+?))(?:-v(?P<version>\d+))?$"
)


__all__ = [
    "registry",
    "current_namespace",
    "ModelSpec",
    "WrapperSpec",
    "VectorizeMode",
    # Functions
    "register",
    "make",
    #"make_vec",
    "spec",
    #"pprint_registry",
    "register_envs",
]


class ModelCreator(Protocol):
    """Function type expected for an environment."""

    def __call__(self, **kwargs: Any) -> Model: ...


# class VectorModelCreator(Protocol):
#      """Function type expected for an environment."""

#      def __call__(self, **kwargs: Any) -> VectorEnv: ...


@dataclass
class WrapperSpec:
    """A specification for recording wrapper configs.

    * name: The name of the wrapper.
    * entry_point: The location of the wrapper to create from.
    * kwargs: Additional keyword arguments passed to the wrapper. If the wrapper doesn't inherit from EzPickle then this is ``None``
    """

    name: str
    entry_point: str
    kwargs: dict[str, Any] | None


@dataclass
class ModelSpec:
    id: str
    entry_point: ModelCreator | str | None = field(default=None)

    # Environment attributes
    reward_threshold: float | None = field(default=None)
    nondeterministic: bool = field(default=False)

    # Wrappers
    max_episode_steps: int | None = field(default=None)
    order_enforce: bool = field(default=True)
    disable_model_checker: bool = field(default=False)

    # Environment arguments
    kwargs: dict = field(default_factory=dict)

    # post-init attributes
    namespace: str | None = field(init=False)
    name: str = field(init=False)
    version: int | None = field(init=False)

    # applied wrappers
    additional_wrappers: tuple[WrapperSpec, ...] = field(default_factory=tuple)

    # Vectorized environment entry point
    # vector_entry_point: VectorModelCreator | str | None = field(default=None)

    def __post_init__(self):
        """Calls after the spec is created to extract the namespace, name and version from the environment id."""
        self.namespace, self.name, self.version = parse_model_id(self.id)

    def make(self, **kwargs: Any) -> Model:
        """Calls ``make`` using the environment spec and any keyword arguments."""
        return make(self, **kwargs)

    def to_json(self) -> str:
        """Converts the environment spec into a json compatible string.

        Returns:
            A jsonifyied string for the environment spec
        """
        model_spec_dict = dataclasses.asdict(self)
        # As the namespace, name and version are initialised after `init` then we remove the attributes
        model_spec_dict.pop("namespace")
        model_spec_dict.pop("name")
        model_spec_dict.pop("version")

        # To check that the environment spec can be transformed to a json compatible type
        self._check_can_jsonify(model_spec_dict)

        return json.dumps(model_spec_dict)

    @staticmethod
    def _check_can_jsonify(model_spec: dict[str, Any]):
        """Warns the user about serialisation failing if the spec contains a callable.

        Args:
            model_spec: An environment or wrapper specification.

        Returns: The specification with lambda functions converted to strings.

        """
        spec_name = model_spec["name"] if "name" in model_spec else model_spec["id"]

        for key, value in model_spec.items():
            if callable(value):
                raise ValueError(
                    f"Callable found in {spec_name} for {key} attribute with value={value}. Currently, not supporting serialising callables."
                )

    @staticmethod
    def from_json(json_model_spec: str) -> ModelSpec:
        parsed_model_spec = json.loads(json_model_spec)

        applied_wrapper_specs: list[WrapperSpec] = []
        for wrapper_spec_json in parsed_model_spec.pop("additional_wrappers"):
            try:
                applied_wrapper_specs.append(WrapperSpec(**wrapper_spec_json))
            except Exception as e:
                raise ValueError(
                    f"An issue occurred when trying to make {wrapper_spec_json} a WrapperSpec"
                ) from e

        try:
            model_spec = ModelSpec(**parsed_model_spec)
            model_spec.additional_wrappers = tuple(applied_wrapper_specs)
        except Exception as e:
            raise ValueError(
                f"An issue occurred when trying to make {parsed_model_spec} an ModelSpec"
            ) from e

        return model_spec

    def pprint(
        self,
        disable_print: bool = False,
        include_entry_points: bool = False,
        print_all: bool = False,
    ) -> str | None:
        """Pretty prints the environment spec.

        Args:
            disable_print: If to disable print and return the output
            include_entry_points: If to include the entry_points in the output
            print_all: If to print all information, including variables with default values

        Returns:
            If ``disable_print is True`` a string otherwise ``None``
        """
        output = f"id={self.id}"
        if print_all or include_entry_points:
            output += f"\nentry_point={self.entry_point}"

        if print_all or self.reward_threshold is not None:
            output += f"\nreward_threshold={self.reward_threshold}"
        if print_all or self.nondeterministic is not False:
            output += f"\nnondeterministic={self.nondeterministic}"

        if print_all or self.max_episode_steps is not None:
            output += f"\nmax_episode_steps={self.max_episode_steps}"
        if print_all or self.order_enforce is not True:
            output += f"\norder_enforce={self.order_enforce}"
        if print_all or self.disable_model_checker is not False:
            output += f"\ndisable_env_checker={self.disable_model_checker}"

        if print_all or self.additional_wrappers:
            wrapper_output: list[str] = []
            for wrapper_spec in self.additional_wrappers:
                if include_entry_points:
                    wrapper_output.append(
                        f"\n\tname={wrapper_spec.name}, entry_point={wrapper_spec.entry_point}, kwargs={wrapper_spec.kwargs}"
                    )
                else:
                    wrapper_output.append(
                        f"\n\tname={wrapper_spec.name}, kwargs={wrapper_spec.kwargs}"
                    )

            if len(wrapper_output) == 0:
                output += "\nadditional_wrappers=[]"
            else:
                output += f"\nadditional_wrappers=[{','.join(wrapper_output)}\n]"

        if disable_print:
            return output
        else:
            print(output)
            return None


class VectorizeMode(Enum):
    """All possible vectorization modes used in `make_vec`."""

    ASYNC = "async"
    SYNC = "sync"
    VECTOR_ENTRY_POINT = "vector_entry_point"


# Global registry of environments. Meant to be accessed through `register` and `make`
registry: dict[str, ModelSpec] = {}
current_namespace: str | None = None


def parse_model_id(model_id: str) -> tuple[str | None, str, int | None]:
    """Parse environment ID string format - ``[namespace/](env-name)[-v(version)]`` where the namespace and version are optional.

    Args:
        model_id: The environment id to parse

    Returns:
        A tuple of environment namespace, environment name and version number

    Raises:
        Error: If the environment id is not valid environment regex
    """
    match = MODEL_ID_RE.fullmatch(model_id)
    if not match:
        raise Exception(
            f"Malformed environment ID: {model_id}. (Currently all IDs must be of the form [namespace/](env-name)-v(version). (namespace is optional))"
        )
    ns, name, version = match.group("namespace", "name", "version")
    if version is not None:
        version = int(version)

    return ns, name, version


def get_model_id(ns: str | None, name: str, version: int | None) -> str:
    """Get the full  ID given a name and (optional) version and namespace. Inverse of :meth:`parse_model_id`.

    Args:
        ns: The environment namespace
        name: The environment name
        version: The environment version

    Returns:
        The environment id
    """
    full_name = name
    if ns is not None:
        full_name = f"{ns}/{name}"
    if version is not None:
        full_name = f"{full_name}-v{version}"

    return full_name


def find_highest_version(ns: str | None, name: str) -> int | None:
    """Finds the highest registered version of the environment given the namespace and name in the registry.

    Args:
        ns: The environment namespace
        name: The environment name (id)

    Returns:
        The highest version of an environment with matching namespace and name, otherwise ``None`` is returned.
    """
    version: list[int] = [
        model_spec.version
        for model_spec in registry.values()
        if model_spec.namespace == ns
        and model_spec.name == name
        and model_spec.version is not None
    ]
    return max(version, default=None)


def _check_namespace_exists(ns: str | None):
    """Check if a namespace exists. If it doesn't, print a helpful error message."""
    # If the namespace is none, then the namespace does exist
    if ns is None:
        return

    # Check if the namespace exists in one of the registry's specs
    namespaces: set[str] = {
        model_spec.namespace
        for model_spec in registry.values()
        if model_spec.namespace is not None
    }
    if ns in namespaces:
        return

    # Otherwise, the namespace doesn't exist and raise a helpful message
    suggestion = (
        difflib.get_close_matches(ns, namespaces, n=1) if len(namespaces) > 0 else None
    )
    if suggestion:
        suggestion_msg = f"Did you mean: `{suggestion[0]}`?"
    else:
        suggestion_msg = f"Have you installed the proper package for {ns}?"

    raise Exception(f"Namespace {ns} not found. {suggestion_msg}")


def _check_name_exists(ns: str | None, name: str):
    """Check if an env exists in a namespace. If it doesn't, print a helpful error message."""
    # First check if the namespace exists
    _check_namespace_exists(ns)

    # Then check if the name exists
    names: set[str] = {
        model_spec.name for model_spec in registry.values() if model_spec.namespace == ns
    }
    if name in names:
        return

    # Otherwise, raise a helpful error to the user
    suggestion = difflib.get_close_matches(name, names, n=1)
    namespace_msg = f" in namespace {ns}" if ns else ""
    suggestion_msg = f" Did you mean: `{suggestion[0]}`?" if suggestion else ""

    raise Exception(
        f"Environment `{name}` doesn't exist{namespace_msg}.{suggestion_msg}"
    )


def _check_version_exists(ns: str | None, name: str, version: int | None):
    """Check if an env version exists in a namespace. If it doesn't, print a helpful error message.

    This is a complete test whether an environment identifier is valid, and will provide the best available hints.

    Args:
        ns: The environment namespace
        name: The environment space
        version: The environment version

    Raises:
        DeprecatedEnv: The environment doesn't exist but a default version does
        VersionNotFound: The ``version`` used doesn't exist
        DeprecatedEnv: Environment version is deprecated
    """
    if get_model_id(ns, name, version) in registry:
        return

    _check_name_exists(ns, name)
    if version is None:
        return

    message = f"Environment version `v{version}` for environment `{get_model_id(ns, name, None)}` doesn't exist."

    model_specs = [
        model_spec
        for model_spec in registry.values()
        if model_spec.namespace == ns and model_spec.name == name
    ]
    model_specs = sorted(model_specs, key=lambda model_spec: int(model_spec.version or -1))

    default_spec = [model_spec for model_spec in model_specs if model_spec.version is None]

    if default_spec:
        message += f" It provides the default version `{default_spec[0].id}`."
        if len(model_specs) == 1:
            raise Exception(message)

    # Process possible versioned environments

    versioned_specs = [
        model_spec for model_spec in model_specs if model_spec.version is not None
    ]

    latest_spec = max(versioned_specs, key=lambda model_spec: model_spec.version, default=None)  # type: ignore
    assert isinstance(latest_spec, ModelSpec) and latest_spec.version is not None, f"latest_spec is not a ModelSpec or version is None > {latest_spec}"
    if latest_spec is not None and version > latest_spec.version:
        version_list_msg = ", ".join(f"`v{model_spec.version}`" for model_spec in model_specs)
        message += f" It provides versioned environments: [ {version_list_msg} ]."

        raise Exception(message)

    if latest_spec is not None and version < latest_spec.version:
        raise Exception(
            f"Environment version v{version} for `{get_model_id(ns, name, None)}` is deprecated. "
            f"Please use `{latest_spec.id}` instead."
        )


def _check_spec_register(testing_spec: ModelSpec):
    """Checks whether the spec is valid to be registered. Helper function for `register`."""
    latest_versioned_spec = max(
        (
            model_spec
            for model_spec in registry.values()
            if model_spec.namespace == testing_spec.namespace
            and model_spec.name == testing_spec.name
            and model_spec.version is not None
        ),
        key=lambda spec_: int(spec_.version),  # type: ignore
        default=None,
    )

    unversioned_spec = next(
        (
            model_spec
            for model_spec in registry.values()
            if model_spec.namespace == testing_spec.namespace
            and model_spec.name == testing_spec.name
            and model_spec.version is None
        ),
        None,
    )

    if unversioned_spec is not None and testing_spec.version is not None:
        raise Exception(
            "Can't register the versioned environment "
            f"`{testing_spec.id}` when the unversioned environment "
            f"`{unversioned_spec.id}` of the same name already exists."
        )
    elif latest_versioned_spec is not None and testing_spec.version is None:
        raise Exception(
            f"Can't register the unversioned environment `{testing_spec.id}` when the versioned environment "
            f"`{latest_versioned_spec.id}` of the same name already exists. Note: the default behavior is "
            "that `make` with the unversioned environment will return the latest versioned environment"
        )


def _check_metadata(testing_metadata: dict[str, Any]):
    """Check the metadata of an environment."""
    if not isinstance(testing_metadata, dict):
        raise Exception(
            f"Expect the environment metadata to be dict, actual type: {type(metadata)}"
        )

    render_modes = testing_metadata.get("render_modes")
    if render_modes is None:
        print(
            f"The environment creator metadata doesn't include `render_modes`, contains: {list(testing_metadata.keys())}"
        )
    elif not isinstance(render_modes, Iterable):
        print(
            f"Expects the environment metadata render_modes to be a Iterable, actual type: {type(render_modes)}"
        )


def _find_spec(model_id: str) -> ModelSpec:
    # For string id's, load the environment spec from the registry then make the environment spec
    assert isinstance(model_id, str)

    # The environment name can include an unloaded module in "module:model_name" style
    module, model_name = (None, model_id) if ":" not in model_id else model_id.split(":")
    if module is not None:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"{e}. Environment registration via importing a module failed. "
                f"Check whether '{module}' contains env registration and can be imported."
            ) from e

    # load the env spec from the registry
    assert model_name is not None, "model_name is None"
    model_spec = registry.get(model_name)

    # update env spec is not version provided, raise warning if out of date
    ns, name, version = parse_model_id(model_name)

    latest_version = find_highest_version(ns, name)
    if version is not None and latest_version is not None and latest_version > version:
        print(
            f"The environment {model_name} is out of date. You should consider "
            f"upgrading to version `v{latest_version}`."
        )
    if version is None and latest_version is not None:
        version = latest_version
        new_model_id = get_model_id(ns, name, version)
        model_spec = registry.get(new_model_id)
        print(
            f"Using the latest versioned environment `{new_model_id}` "
            f"instead of the unversioned environment `{model_name}`."
        )

    if model_spec is None:
        _check_version_exists(ns, name, version)
        raise Exception(
            f"No registered env with id: {model_name}. Did you register it, or import the package that registers it? Use `pprint_registry()` to see all of the registered environments."
        )

    return model_spec


def load_env_creator(name: str) -> ModelCreator :#| VectorModelCreator:
    """Loads an environment with name of style ``"(import path):(environment name)"`` and returns the environment creation function, normally the environment class type.

    Args:
        name: The environment name

    Returns:
        The environment constructor for the given environment name.
    """
    mod_name, attr_name = name.split(":")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr_name)
    return fn


def register_envs(env_module: ModuleType):
    """A No-op function such that it can appear to IDEs that a module is used."""
    pass


@contextlib.contextmanager
def namespace(ns: str):
    """Context manager for modifying the current namespace."""
    global current_namespace
    old_namespace = current_namespace
    current_namespace = ns
    yield
    current_namespace = old_namespace


def register(
    id: str,
    entry_point: ModelCreator | str | None = None,
    reward_threshold: float | None = None,
    nondeterministic: bool = False,
    max_episode_steps: int | None = None,
    order_enforce: bool = True,
    disable_model_checker: bool = False,
    additional_wrappers: tuple[WrapperSpec, ...] = (),
    vector_entry_point: str | None = None, #VectorModelCreator | str | None = None,
    kwargs: dict | None = None,
):
    assert (
        entry_point is not None or vector_entry_point is not None
    ), "Either `entry_point` or `vector_entry_point` (or both) must be provided"
    global registry, current_namespace
    ns, name, version = parse_model_id(id)

    if kwargs is None:
        kwargs = dict()
    if current_namespace is not None:
        if (
            kwargs.get("namespace") is not None
            and kwargs.get("namespace") != current_namespace
        ):
            print(
                f"Custom namespace `{kwargs.get('namespace')}` is being overridden by namespace `{current_namespace}`. "
                f"If you are developing a plugin you shouldn't specify a namespace in `register` calls. "
                "The namespace is specified through the entry point package metadata."
            )
        ns_id: str | None = current_namespace
    else:
        #assert ns is not None, "Namespace must be provided"
        ns_id = ns
    full_model_id = get_model_id(ns_id, name, version)

    new_spec = ModelSpec(
        id=full_model_id,
        entry_point=entry_point,
        reward_threshold=reward_threshold,
        nondeterministic=nondeterministic,
        max_episode_steps=max_episode_steps,
        order_enforce=order_enforce,
        disable_model_checker=disable_model_checker,
        kwargs=kwargs,
        additional_wrappers=additional_wrappers,
        #vector_entry_point=vector_entry_point,
    )
    _check_spec_register(new_spec)

    if new_spec.id in registry:
        print(f"Overriding environment {new_spec.id} already in registry.")
    registry[new_spec.id] = new_spec


def make(
    id: str | ModelSpec,
    max_episode_steps: int | None = None,
    disable_model_checker: bool | None = None,
    **kwargs: Any,
) -> Model:
    if isinstance(id, ModelSpec):
        model_spec = id
        if not hasattr(model_spec, "additional_wrappers"):
            print(
                f"The env spec passed to `make` does not have a `additional_wrappers`, set it to an empty tuple. model_spec={model_spec}"
            )
            model_spec.additional_wrappers = ()
    else:
        # For string id's, load the environment spec from the registry then make the environment spec
        assert isinstance(id, str)

        # The environment name can include an unloaded module in "module:model_name" style
        model_spec = _find_spec(id)

    assert isinstance(model_spec, ModelSpec)

    # Update the env spec kwargs with the `make` kwargs
    model_spec_kwargs = copy.deepcopy(model_spec.kwargs)
    model_spec_kwargs.update(kwargs)

    # Load the environment creator
    if model_spec.entry_point is None:
        raise ValueError(f"{model_spec.id} registered but entry_point is not specified")
    elif callable(model_spec.entry_point):
        env_creator = model_spec.entry_point
    else:
        # Assume it's a string
        env_creator = load_env_creator(model_spec.entry_point) # type: ignore

    # Determine if to use the rendering
    render_modes: list[str] | None = None
    if hasattr(env_creator, "metadata"):
        _check_metadata(env_creator.metadata)
        render_modes = env_creator.metadata.get("render_modes")
    render_mode = model_spec_kwargs.get("render_mode")
    apply_human_rendering = False
    apply_render_collection = False

    # If mode is not valid, try applying HumanRendering/RenderCollection wrappers
    if (
        render_mode is not None
        and render_modes is not None
        and render_mode not in render_modes
    ):
        displayable_modes = {"rgb_array", "rgb_array_list"}.intersection(render_modes)
        if render_mode == "human" and len(displayable_modes) > 0:
            print(
                "You are trying to use 'human' rendering for an environment that doesn't natively support it. "
                "The HumanRendering wrapper is being applied to your environment."
            )
            model_spec_kwargs["render_mode"] = displayable_modes.pop()
            apply_human_rendering = True
        elif (
            render_mode.endswith("_list")
            and render_mode[: -len("_list")] in render_modes
        ):
            model_spec_kwargs["render_mode"] = render_mode[: -len("_list")]
            apply_render_collection = True
        else:
            print(
                f"The environment is being initialised with render_mode={render_mode!r} "
                f"that is not in the possible render_modes ({render_modes})."
            )

    try:
        model = env_creator(**model_spec_kwargs)
    except TypeError as e:
        if (
            str(e).find("got an unexpected keyword argument 'render_mode'") >= 0
            and apply_human_rendering
        ):
            raise Exception(
                f"You passed render_mode='human' although {model_spec.id} doesn't implement human-rendering natively. "
            ) from e
        else:
            raise type(e)(
                f"{e} was raised from the environment creator for {model_spec.id} with kwargs ({model_spec_kwargs})"
            )

    if not isinstance(model, Model):
        raise TypeError(
            f"The environment must inherit from the Model class, actual class: {type(model)}"
        )

    # Set the minimal model spec for the environment.
    model.unwrapped.model_spec = ModelSpec(
        id=model_spec.id,
        entry_point=model_spec.entry_point, # type: ignore[arg-type]
        reward_threshold=model_spec.reward_threshold,
        nondeterministic=model_spec.nondeterministic,
        max_episode_steps=None,
        order_enforce=False,
        disable_model_checker=True,
        kwargs=model_spec_kwargs,
        additional_wrappers=(),
        #vector_entry_point=model_spec.vector_entry_point,
    )

    # Check if pre-wrapped wrappers
    assert model.model_spec is not None
    num_prior_wrappers = len(model.model_spec.additional_wrappers)
    if (
        model_spec.additional_wrappers[:num_prior_wrappers]
        != model.model_spec.additional_wrappers
    ):
        for model_spec_wrapper_spec, recreated_wrapper_spec in zip(
            model_spec.additional_wrappers, model.model_spec.additional_wrappers
        ):
            raise ValueError(
                f"The environment's wrapper spec {recreated_wrapper_spec} is different from the saved `ModelSpec` additional wrapper {model_spec_wrapper_spec}"
            )

    # Run the environment checker as the lowest level wrapper
    if disable_model_checker is False or (
        disable_model_checker is None and model_spec.disable_model_checker is False
    ):
        model = wrappers.PassiveEnvChecker(model)

    # Add the order enforcing wrapper
    if model_spec.order_enforce:
        model = wrappers.OrderEnforcing(model)

    # Add the time limit wrapper
    if max_episode_steps != -1:
        if max_episode_steps is not None:
            model = wrappers.TimeLimit(model, max_episode_steps)
        elif model_spec.max_episode_steps is not None:
            model = wrappers.TimeLimit(model, model_spec.max_episode_steps)

    for wrapper_spec in model_spec.additional_wrappers[num_prior_wrappers:]:
        if wrapper_spec.kwargs is None:
            raise ValueError(
                f"{wrapper_spec.name} wrapper does not inherit from `gymnasium.utils.RecordConstructorArgs`, therefore, the wrapper cannot be recreated."
            )

        model = load_env_creator(wrapper_spec.entry_point)(env=model, **wrapper_spec.kwargs) # type: ignore

    # Add human rendering wrapper
    # if apply_human_rendering:
    #     model = wrappers.HumanRendering(model)
    # elif apply_render_collection:
    #     model = wrappers.RenderCollection(model)

    return model


# def make_vec(
#     id: str | ModelSpec,
#     num_envs: int = 1,
#     vectorization_mode: VectorizeMode | str | None = None,
#     vector_kwargs: dict[str, Any] | None = None,
#     wrappers: Sequence[Callable[[Model], Wrapper]] | None = None,
#     **kwargs,
# ) -> VectorEnv:
#     """Create a vector environment according to the given ID.

#     To find all available environments use :func:`gymnasium.pprint_registry` or ``gymnasium.registry.keys()`` for all valid ids.
#     We refer to the Vector environment as the vectorizor while the environment being vectorized is the base or vectorized environment (``vectorizor(vectorized env)``).

#     Args:
#         id: Name of the environment. Optionally, a module to import can be included, e.g. 'module:Env-v0'
#         num_envs: Number of environments to create
#         vectorization_mode: The vectorization method used, defaults to ``None`` such that if env id' spec has a ``vector_entry_point`` (not ``None``),
#             this is first used otherwise defaults to ``sync`` to use the :class:`gymnasium.vector.SyncVectorEnv`.
#             Valid modes are ``"async"``, ``"sync"`` or ``"vector_entry_point"``. Recommended to use the :class:`VectorizeMode` enum rather than strings.
#         vector_kwargs: Additional arguments to pass to the vectorizor environment constructor, i.e., ``SyncVectorEnv(..., **vector_kwargs)``.
#         wrappers: A sequence of wrapper functions to apply to the base environment. Can only be used in ``"sync"`` or ``"async"`` mode.
#         **kwargs: Additional arguments passed to the base environment constructor.

#     Returns:
#         An instance of the environment.

#     Raises:
#         Error: If the ``id`` doesn't exist then an error is raised
#     """
#     if vector_kwargs is None:
#         vector_kwargs = {}
#     if wrappers is None:
#         wrappers = []

#     if isinstance(id, ModelSpec):
#         model_spec = id
#     elif isinstance(id, str):
#         model_spec = _find_spec(id)
#     else:
#         raise Exception(f"Invalid id type: {type(id)}. Expected `str` or `ModelSpec`")

#     model_spec = copy.deepcopy(model_spec)
#     model_spec_kwargs = model_spec.kwargs
#     # for sync or async, these parameters should be passed in `make(..., **kwargs)` rather than in the env spec kwargs, therefore, we `reset` the kwargs
#     model_spec.kwargs = dict()

#     num_envs = model_spec_kwargs.pop("num_envs", num_envs)
#     vectorization_mode = model_spec_kwargs.pop("vectorization_mode", vectorization_mode)
#     vector_kwargs = model_spec_kwargs.pop("vector_kwargs", vector_kwargs)
#     wrappers = model_spec_kwargs.pop("wrappers", wrappers)

#     model_spec_kwargs.update(kwargs)

#     # Specify the vectorization mode if None or update to a `VectorizeMode`
#     if vectorization_mode is None:
#         if model_spec.vector_entry_point is not None:
#             vectorization_mode = VectorizeMode.VECTOR_ENTRY_POINT
#         else:
#             vectorization_mode = VectorizeMode.SYNC
#     else:
#         try:
#             vectorization_mode = VectorizeMode(vectorization_mode)
#         except ValueError:
#             raise ValueError(
#                 f"Invalid vectorization mode: {vectorization_mode!r}, "
#                 f"valid modes: {[mode.value for mode in VectorizeMode]}"
#             )
#     assert isinstance(vectorization_mode, VectorizeMode)

#     def create_single_env() -> Model:
#         single_model = make(model_spec, **model_spec_kwargs.copy())

#         if wrappers is None:
#             return single_model

#         for wrapper in wrappers:
#             single_model = wrapper(single_model)
#         return single_model

#     if vectorization_mode == VectorizeMode.SYNC:
#         if model_spec.entry_point is None:
#             raise Exception(
#                 f"Cannot create vectorized environment for {model_spec.id} because it doesn't have an entry point defined."
#             )

#         env = SyncVectorEnv(
#             env_fns=(create_single_env for _ in range(num_envs)),
#             **vector_kwargs,
#         )
#     elif vectorization_mode == VectorizeMode.ASYNC:
#         if model_spec.entry_point is None:
#             raise Exception(
#                 f"Cannot create vectorized environment for {model_spec.id} because it doesn't have an entry point defined."
#             )

#         env = AsyncVectorEnv(
#             env_fns=[create_single_env for _ in range(num_envs)],
#             **vector_kwargs,
#         )

#     if vectorization_mode == VectorizeMode.VECTOR_ENTRY_POINT:
#         if len(vector_kwargs) > 0:
#             raise Exception(
#                 f"Custom vector environment can be passed arguments only through kwargs and `vector_kwargs` is not empty ({vector_kwargs})"
#             )
#         elif len(wrappers) > 0:
#             raise Exception(
#                 f"Cannot use `vector_entry_point` vectorization mode with the wrappers argument ({wrappers})."
#             )
#         elif len(model_spec.additional_wrappers) > 0:
#             raise Exception(
#                 f"Cannot use `vector_entry_point` vectorization mode with the additional_wrappers parameter in spec being not empty ({model_spec.additional_wrappers})."
#             )

#         entry_point = model_spec.vector_entry_point
#         if entry_point is None:
#             raise Exception(
#                 f"Cannot create vectorized environment for {id} because it doesn't have a vector entry point defined."
#             )
#         elif callable(entry_point):
#             env_creator = entry_point
#         else:  # Assume it's a string
#             env_creator = load_env_creator(entry_point)

#         if (
#             model_spec.max_episode_steps is not None
#             and "max_episode_steps" not in model_spec_kwargs
#         ):
#             model_spec_kwargs["max_episode_steps"] = model_spec.max_episode_steps

#         env = env_creator(num_envs=num_envs, **model_spec_kwargs)
#     else:
#         raise Exception(f"Unknown vectorization mode: {vectorization_mode}")

#     # Copies the environment creation specification and kwargs to add to the environment specification details
#     copied_id_spec = copy.deepcopy(model_spec)
#     copied_id_spec.kwargs = model_spec_kwargs
#     if num_envs != 1:
#         copied_id_spec.kwargs["num_envs"] = num_envs
#     copied_id_spec.kwargs["vectorization_mode"] = vectorization_mode.value
#     if len(vector_kwargs) > 0:
#         copied_id_spec.kwargs["vector_kwargs"] = vector_kwargs
#     if len(wrappers) > 0:
#         copied_id_spec.kwargs["wrappers"] = wrappers
#     env.unwrapped.model_spec = copied_id_spec

#     return env


def spec(model_id: str) -> ModelSpec:
    """Retrieve the :class:`ModelSpec` for the environment id from the :attr:`registry`.

    Args:
        model_id: The environment id with the expected format of ``[(namespace)/]id[-v(version)]``

    Returns:
        The environment spec if it exists

    Raises:
        Error: If the environment id doesn't exist
    """
    model_spec = registry.get(model_id)
    if model_spec is None:
        ns, name, version = parse_model_id(model_id)
        _check_version_exists(ns, name, version)
        raise Exception(f"No registered env with id: {model_id}")
    else:
        assert isinstance(
            model_spec, ModelSpec
        ), f"Expected the registry for {model_id} to be an `ModelSpec`, actual type is {type(model_spec)}"
        return model_spec

