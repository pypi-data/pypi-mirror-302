from __future__ import annotations

import time
from collections import deque
from copy import deepcopy
from typing import TYPE_CHECKING, Any, SupportsFloat

from maspy.learning.core import Model, Wrapper
from maspy.learning.core import ActType, ObsType, RenderFrame, WrapperObsType
from maspy.learning.ml_utils import (
    RecordConstructorArgs,
    check_action_space,
    check_observation_space,
    env_render_passive_checker,
    env_reset_passive_checker,
    env_step_passive_checker,
)


if TYPE_CHECKING:
    from maspy.learning.registration import ModelSpec


__all__ = [
    "TimeLimit",
    "Autoreset",
    "PassiveEnvChecker",
    "OrderEnforcing",
    "RecordEpisodeStatistics",
]


class TimeLimit(Wrapper[ObsType, ActType, ObsType, ActType], RecordConstructorArgs
):
    """Provides a time limit on the number of steps for an environment before it truncates."""

    def __init__(
        self,
        model: Model,
        max_episode_steps: int,
    ):
        RecordConstructorArgs.__init__(
            self, max_episode_steps=max_episode_steps
        )
        Wrapper.__init__(self, model)

        self._max_episode_steps = max_episode_steps
        self._elapsed_steps: int | None = None

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """Steps through the environment and if the number of steps elapsed exceeds ``max_episode_steps`` then truncate.

        Args:
            action: The environment step action

        Returns:
            The environment step ``(observation, reward, terminated, truncated, info)`` with `truncated=True`
            if the number of steps elapsed >= max episode steps

        """
        observation, reward, terminated, truncated, info = self.env_model.step(action)
        assert self._elapsed_steps is not None, "elapsed_steps should not be None during step" 
        self._elapsed_steps += 1

        if self._elapsed_steps >= self._max_episode_steps:
            truncated = True

        return observation, reward, terminated, truncated, info

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[ObsType, dict[str, Any]]:
        """Resets the environment with :param:`**kwargs` and sets the number of steps elapsed to zero.

        Args:
            seed: Seed for the environment
            options: Options for the environment

        Returns:
            The reset environment
        """
        self._elapsed_steps = 0
        return super().reset(seed=seed, options=options)

    @property
    def spec(self) -> ModelSpec | None:
        """Modifies the environment spec to include the `max_episode_steps=self._max_episode_steps`."""
        if self._cached_spec is not None:
            return self._cached_spec

        env_spec = self.env_model.model_spec
        if env_spec is not None:
            try:
                env_spec = deepcopy(env_spec)
                env_spec.max_episode_steps = self._max_episode_steps
            except Exception as e:
                print(
                    f"An exception occurred ({e}) while copying the environment spec={env_spec}"
                )
                return None

        self._cached_spec = env_spec
        return env_spec


class Autoreset(
    Wrapper[ObsType, ActType, ObsType, ActType], RecordConstructorArgs
):
    def __init__(self, env: Model):
        RecordConstructorArgs.__init__(self)
        Wrapper.__init__(self, env)

        self.autoreset = False

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[WrapperObsType, dict[str, Any]]:
        """Resets the environment and sets autoreset to False preventing."""
        self.autoreset = False
        return super().reset(seed=seed, options=options) # type: ignore[return-value]

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """Steps through the environment with action and resets the environment if a terminated or truncated signal is encountered.
        
        Args:
            action: The action to take

        Returns:
            The autoreset environment :meth:`step`
        """
        if self.autoreset:
            obs, info = self.env_model.reset()
            reward, terminated, truncated = 0.0, False, False
        else:
            obs, reward, terminated, truncated, info = self.env_model.step(action) # type: ignore[assignment] # SupportsFloat mess

        self.autoreset = terminated or truncated
        return obs, reward, terminated, truncated, info


class PassiveEnvChecker(
    Wrapper[ObsType, ActType, ObsType, ActType], RecordConstructorArgs
):

    def __init__(self, env: Model[ObsType, ActType]):
        """Initialises the wrapper with the environments, run the observation and action space tests."""
        RecordConstructorArgs.__init__(self)
        Wrapper.__init__(self, env)

        if not isinstance(env, Model):
            if str(env.__class__.__base__) == "<class 'gym.core.Env'>":
                raise TypeError(
                    "Gym is incompatible with Gymnasium, please update the environment class to `gymnasium.Env`. "
                    "See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
                )
            else:
                raise TypeError(
                    f"The environment must inherit from the gymnasium.Env class, actual class: {type(env)}. "
                    "See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
                )

        if not hasattr(env, "action_space"):
            raise AttributeError(
                "The environment must specify an action space. https://gymnasium.farama.org/introduction/create_custom_env/"
            )
        check_action_space(env.action_space)

        if not hasattr(env, "observation_space"):
            raise AttributeError(
                "The environment must specify an observation space. https://gymnasium.farama.org/introduction/create_custom_env/"
            )
        check_observation_space(env.observation_space)

        self.checked_reset: bool = False
        self.checked_step: bool = False
        self.checked_render: bool = False
        self.close_called: bool = False

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """Steps through the environment that on the first call will run the `passive_env_step_check`."""
        if self.checked_step is False:
            self.checked_step = True
            return env_step_passive_checker(self.env_model, action)
        else:
            return self.env_model.step(action)

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[ObsType, dict[str, Any]]:
        """Resets the environment that on the first call will run the `passive_env_reset_check`."""
        if self.checked_reset is False:
            self.checked_reset = True
            return env_reset_passive_checker(self.env_model, seed=seed, options=options)
        else:
            return self.env_model.reset(seed=seed, options=options)

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        """Renders the environment that on the first call will run the `passive_env_render_check`."""
        if self.checked_render is False:
            self.checked_render = True
            return env_render_passive_checker(self.env_model)
        else:
            return self.env_model.render()

    @property
    def spec(self) -> ModelSpec | None:
        """Modifies the environment spec to such that `disable_env_checker=False`."""
        if self._cached_spec is not None:
            return self._cached_spec

        env_spec = self.env_model.model_spec
        if env_spec is not None:
            try:
                env_spec = deepcopy(env_spec)
                env_spec.disable_model_checker = False
            except Exception as e:
                print(
                    f"An exception occurred ({e}) while copying the environment spec={env_spec}"
                )
                return None

        self._cached_spec = env_spec
        return env_spec

    def close(self):
        """Warns if calling close on a closed environment fails."""
        if not self.close_called:
            self.close_called = True
            return self.env_model.close()
        else:
            try:
                return self.env_model.close()
            except Exception as e:
                print(
                    "Calling `env.close()` on the closed environment should be allowed, but it raised the following exception."
                )
                raise e


class OrderEnforcing(
    Wrapper[ObsType, ActType, ObsType, ActType], RecordConstructorArgs
):
    """Will produce an error if ``step`` or ``render`` is called before ``reset``.

    No vector version of the wrapper exists.

    Example:
        >>> import gymnasium as gym
        >>> from gymnasium.wrappers import OrderEnforcing
        >>> env = gym.make("CartPole-v1", render_mode="human")
        >>> env = OrderEnforcing(env)
        >>> env.step(0)
        Traceback (most recent call last):
            ...
        gymnasium.error.ResetNeeded: Cannot call env.step() before calling env.reset()
        >>> env.render()
        Traceback (most recent call last):
            ...
        gymnasium.error.ResetNeeded: Cannot call `env.render()` before calling `env.reset()`, if this is an intended action, set `disable_render_order_enforcing=True` on the OrderEnforcer wrapper.
        >>> _ = env.reset()
        >>> env.render()
        >>> _ = env.step(0)
        >>> env.close()

    Change logs:
     * v0.22.0 - Initially added
     * v0.24.0 - Added order enforcing for the render function
    """

    def __init__(
        self,
        model: Model[ObsType, ActType],
        disable_render_order_enforcing: bool = False,
    ):
        """A wrapper that will produce an error if :meth:`step` is called before an initial :meth:`reset`.

        Args:
            env: The environment to wrap
            disable_render_order_enforcing: If to disable render order enforcing
        """
        RecordConstructorArgs.__init__(
            self, disable_render_order_enforcing=disable_render_order_enforcing
        )
        Wrapper.__init__(self, model)

        self._has_reset: bool = False
        self._disable_render_order_enforcing: bool = disable_render_order_enforcing

    def step(self, action: ActType) -> tuple[ObsType, SupportsFloat, bool, bool, dict]:
        """Steps through the environment."""
        if not self._has_reset:
            raise Exception("Cannot call env.step() before calling env.reset()")
        return super().step(action)

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[ObsType, dict[str, Any]]:
        """Resets the environment with `kwargs`."""
        self._has_reset = True
        return super().reset(seed=seed, options=options)

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        """Renders the environment with `kwargs`."""
        if not self._disable_render_order_enforcing and not self._has_reset:
            raise Exception(
                "Cannot call `env.render()` before calling `env.reset()`, if this is an intended action, "
                "set `disable_render_order_enforcing=True` on the OrderEnforcer wrapper."
            )
        return super().render()

    @property
    def has_reset(self):
        """Returns if the environment has been reset before."""
        return self._has_reset

    @property
    def spec(self) -> ModelSpec | None:
        """Modifies the environment spec to add the `order_enforce=True`."""
        if self._cached_spec is not None:
            return self._cached_spec

        env_spec = self.env_model.model_spec
        if env_spec is not None:
            try:
                env_spec = deepcopy(env_spec)
                env_spec.order_enforce = True
            except Exception as e:
                print(
                    f"An exception occurred ({e}) while copying the environment spec={env_spec}"
                )
                return None

        self._cached_spec = env_spec
        return env_spec


class RecordEpisodeStatistics(
    Wrapper[ObsType, ActType, ObsType, ActType], RecordConstructorArgs
):
    """This wrapper will keep track of cumulative rewards and episode lengths.

    At the end of an episode, the statistics of the episode will be added to ``info``
    using the key ``episode``. If using a vectorized environment also the key
    ``_episode`` is used which indicates whether the env at the respective index has
    the episode statistics.
    A vector version of the wrapper exists, :class:`gymnasium.wrappers.vector.RecordEpisodeStatistics`.

    After the completion of an episode, ``info`` will look like this::

        >>> info = {
        ...     "episode": {
        ...         "r": "<cumulative reward>",
        ...         "l": "<episode length>",
        ...         "t": "<elapsed time since beginning of episode>"
        ...     },
        ... }

    For a vectorized environments the output will be in the form of::

        >>> infos = {
        ...     "episode": {
        ...         "r": "<array of cumulative reward>",
        ...         "l": "<array of episode length>",
        ...         "t": "<array of elapsed time since beginning of episode>"
        ...     },
        ...     "_episode": "<boolean array of length num-envs>"
        ... }

    Moreover, the most recent rewards and episode lengths are stored in buffers that can be accessed via
    :attr:`wrapped_env.return_queue` and :attr:`wrapped_env.length_queue` respectively.

    Attributes:
     * time_queue: The time length of the last ``deque_size``-many episodes
     * return_queue: The cumulative rewards of the last ``deque_size``-many episodes
     * length_queue: The lengths of the last ``deque_size``-many episodes

    Change logs:
     * v0.15.4 - Initially added
     * v1.0.0 - Removed vector environment support (see :class:`gymnasium.wrappers.vector.RecordEpisodeStatistics`) and add attribute ``time_queue``
    """

    def __init__(
        self,
        env: Model[ObsType, ActType],
        buffer_length: int = 100,
        stats_key: str = "episode",
    ):
        """This wrapper will keep track of cumulative rewards and episode lengths.

        Args:
            env (Env): The environment to apply the wrapper
            buffer_length: The size of the buffers :attr:`return_queue`, :attr:`length_queue` and :attr:`time_queue`
            stats_key: The info key for the episode statistics
        """
        RecordConstructorArgs.__init__(self)
        Wrapper.__init__(self, env)

        self._stats_key = stats_key

        self.episode_count = 0
        self.episode_start_time: float = -1
        self.episode_returns: float = 0.0
        self.episode_lengths: int = 0

        self.time_queue: deque[float] = deque(maxlen=buffer_length)
        self.return_queue: deque[float] = deque(maxlen=buffer_length)
        self.length_queue: deque[int] = deque(maxlen=buffer_length)

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """Steps through the environment, recording the episode statistics."""
        obs, reward, terminated, truncated, info = super().step(action)
        
        assert isinstance(reward, float | int), f'{reward} should be float or int, not {type(reward)}'
        self.episode_returns += reward
        self.episode_lengths += 1

        if terminated or truncated:
            assert self._stats_key not in info

            episode_time_length = round(
                time.perf_counter() - self.episode_start_time, 6
            )
            info[self._stats_key] = {
                "r": self.episode_returns,
                "l": self.episode_lengths,
                "t": episode_time_length,
            }

            self.time_queue.append(episode_time_length)
            self.return_queue.append(self.episode_returns)
            self.length_queue.append(self.episode_lengths)

            self.episode_count += 1
            self.episode_start_time = time.perf_counter()

        return obs, reward, terminated, truncated, info

    def reset(
        self, *, seed: int | None = None, options: dict[str, Any] | None = None
    ) -> tuple[ObsType, dict[str, Any]]:
        """Resets the environment using seed and options and resets the episode rewards and lengths."""
        obs, info = super().reset(seed=seed, options=options)

        self.episode_start_time = time.perf_counter()
        self.episode_returns = 0.0
        self.episode_lengths = 0

        return obs, info