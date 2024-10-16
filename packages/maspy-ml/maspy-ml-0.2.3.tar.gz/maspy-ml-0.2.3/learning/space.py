import collections.abc
import typing
from typing import Generic, TypeVar, Sequence, Any, SupportsFloat, Iterable, KeysView, Mapping

import numpy as np
from numpy.typing import NDArray
import numpy.typing as npt

from maspy.learning.ml_utils import utl_np_random

Cov_Type = TypeVar("Cov_Type", covariant=True)
RNG = RandomNumberGenerator = np.random.Generator
MaskNDArray = npt.NDArray[np.int8]

__all__ = [
    "Space",
    "Box",
    "Discrete",
    "MultiDiscrete",
    "MultiBinary",
    "Tuple",
    "Dict"
]

class Space(Generic[Cov_Type]):
    def __init__(
            self, 
            shape: Sequence[int] | None = None, 
            dtype: npt.DTypeLike | None = None, 
            seed: int | np.random.Generator | None = None
        ):
        self._shape = None if shape is None else tuple(shape)
        self.dtype = None if dtype is None else np.dtype(dtype)
        
        self._np_random = None
        if seed is not None:
            if isinstance(seed, np.random.Generator):
                self._np_random = seed
            else:
                self.seed(seed)
        
    def seed(self, seed: int | None = None) -> int | list[int] | dict[str, int]:
        self._np_random, np_random_seed = utl_np_random(seed)
        return np_random_seed

    @property
    def np_random(self) -> np.random.Generator:
        if self._np_random is None:
            self.seed()

        if self._np_random is None:
            self._np_random, _ = utl_np_random()

        return self._np_random
    
    @property
    def shape(self) -> tuple[int, ...] | None:
        return self._shape
    
    @property
    def is_np_flattenable(self) -> bool:
        """Checks whether this space can be flattened to a :class:`gymnasium.spaces.Box`."""
        raise NotImplementedError

    def sample(self, mask: Any | None = None) -> Cov_Type:
        """Randomly sample an element of this space.

        Can be uniform or non-uniform sampling based on boundedness of space.

        Args:
            mask: A mask used for sampling, expected ``dtype=np.int8`` and see sample implementation for expected shape.

        Returns:
            A sampled actions from the space
        """
        raise NotImplementedError
    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space, equivalent to ``sample in space``."""
        raise NotImplementedError

    def __contains__(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        return self.contains(x)

    def __setstate__(self, state: Iterable[tuple[str, Any]] | Mapping[str, Any]):
        """Used when loading a pickled space.

        This method was implemented explicitly to allow for loading of legacy states.

        Args:
            state: The updated state value
        """
        # Don't mutate the original state
        state = dict(state)

        if "shape" in state:
            state["_shape"] = state.get("shape")
            del state["shape"]
        if "np_random" in state:
            state["_np_random"] = state["np_random"]
            del state["np_random"]

        # Update our state
        self.__dict__.update(state)
  
def is_float_integer(var: Any) -> bool:
    """Checks if a scalar variable is an integer or float (does not include bool)."""
    return np.issubdtype(type(var), np.integer) or np.issubdtype(type(var), np.floating)

class Box(Space[NDArray[Any]]):
    def __init__(
        self,
        low: SupportsFloat | NDArray[Any],
        high: SupportsFloat | NDArray[Any],
        shape: Sequence[int] | None = None,
        dtype: type[np.floating[Any]] | type[np.integer[Any]] = np.float32,
        seed: int | np.random.Generator | None = None,
    ):
        if dtype is None:
            raise ValueError("Box dtype cannot be None")
        self.dtype = np.dtype(dtype)
        
        if not (
            np.issubdtype(self.dtype, np.floating) 
            or np.issubdtype(self.dtype, np.integer)
            or self.dtype == np.bool_
        ):
            raise ValueError(f"Invalid Box dtype ({self.dtype}). Must be floating, integer or bool")
        
        if shape is not None:
            if not isinstance(shape, Iterable):
                raise TypeError(f"Box shape must be an iterable, actual type: {type(shape)}")
            elif not all(np.issubdtype(type(dim), np.integer) for dim in shape):
                raise TypeError(f"All Box shape elements must be integers, actual type: {type(shape)}")
            shape = tuple(int(dim) for dim in shape)
        elif isinstance(low, np.ndarray) and isinstance(high, np.ndarray):
            if low.shape != high.shape:
                raise ValueError(
                    f"Box low.shape and high.shape don't match, low.shape={low.shape}, high.shape={high.shape}"
                )
            shape = low.shape
        elif isinstance(low, np.ndarray):
            shape = low.shape
        elif isinstance(high, np.ndarray):
            shape = high.shape
        elif is_float_integer(low) and is_float_integer(high):
            shape = (1,)  # low and high are scalars
        else:
            raise ValueError(
                "Box shape is not specified, therefore inferred from low and high. Expected low and high to be np.ndarray, integer, or float."
                f"Actual types low={type(low)}, high={type(high)}"
            )
        self._shape: tuple[int, ...] = shape

        dtype_min: int | float
        dtype_max: int | float
        if self.dtype == np.bool_:
            dtype_min, dtype_max = 0, 1
        elif np.issubdtype(self.dtype, np.floating): 
            dtype_min = float(np.finfo(self.dtype).min)
            dtype_max = float(np.finfo(self.dtype).max)
        elif np.issubdtype(self.dtype, np.integer):
            dtype_min = int(np.iinfo(self.dtype).min)
            dtype_max = int(np.iinfo(self.dtype).max)
        else:
            raise TypeError(f'Unsupported dtype: {self.dtype}')

        self.low, self.bounded_below = self._cast_low(low, dtype_min)
        self.high, self.bounded_above = self._cast_high(high, dtype_max)

        if self.low.shape != shape:
            raise ValueError(
                f"Box low.shape doesn't match provided shape, low.shape={self.low.shape}, shape={self.shape}"
            )
        if self.high.shape != shape:
            raise ValueError(
                f"Box high.shape doesn't match provided shape, high.shape={self.high.shape}, shape={self.shape}"
            )

        # check that low <= high
        if np.any(self.low > self.high):
            raise ValueError(
                f"Box all low values must be less than or equal to high (some values break this), low={self.low}, high={self.high}"
            )

        self.low_repr = str(self.low)
        self.high_repr = str(self.high)

        super().__init__(self.shape, self.dtype, seed)
    
        
    def _cast_low(self, low, dtype_min) -> tuple[np.ndarray, np.ndarray]:
        assert self.dtype is not None, 'Box dtype cannot be None'
        if is_float_integer(low):
            bounded_below = -np.inf < np.full(self.shape, low, dtype=float)

            if np.isnan(low):
                raise ValueError(f"No low value can be equal to `np.nan`, low={low}")
            elif np.isneginf(low):
                if self.dtype.kind == "i":  # signed int
                    low = dtype_min
                elif self.dtype.kind in {"u", "b"}:  # unsigned int and bool
                    raise ValueError(
                        f"Box unsigned int dtype don't support `-np.inf`, low={low}"
                    )
            elif low < dtype_min:
                raise ValueError(
                    f"Box low is out of bounds of the dtype range, low={low}, min dtype={dtype_min}"
                )

            low = np.full(self.shape, low, dtype=self.dtype)
            return low, bounded_below
        else:  # cast for low - array
            if not isinstance(low, np.ndarray):
                raise ValueError(
                    f"Box low must be a np.ndarray, integer, or float, actual type={type(low)}"
                )
            elif not (
                np.issubdtype(low.dtype, np.floating)
                or np.issubdtype(low.dtype, np.integer)
                or low.dtype == np.bool_
            ):
                raise ValueError(
                    f"Box low must be a floating, integer, or bool dtype, actual dtype={low.dtype}"
                )
            elif np.any(np.isnan(low)):
                raise ValueError(f"No low value can be equal to `np.nan`, low={low}")

            bounded_below = -np.inf < low

            if np.any(np.isneginf(low)):
                if self.dtype.kind == "i":  # signed int
                    low[np.isneginf(low)] = dtype_min
                elif self.dtype.kind in {"u", "b"}:  # unsigned int and bool
                    raise ValueError(
                        f"Box unsigned int dtype don't support `-np.inf`, low={low}"
                    )
            elif low.dtype != self.dtype and np.any(low < dtype_min):
                raise ValueError(
                    f"Box low is out of bounds of the dtype range, low={low}, min dtype={dtype_min}"
                )
            
            
            if (
                np.issubdtype(low.dtype, np.floating)
                and np.issubdtype(self.dtype, np.floating)
                and np.finfo(self.dtype).precision < np.finfo(low.dtype).precision
            ):    
                print(
                    f"Box low's precision lowered by casting to {self.dtype}, current low.dtype={low.dtype}"
                )
                
            return low.astype(self.dtype), bounded_below

    def _cast_high(self, high, dtype_max) -> tuple[np.ndarray, np.ndarray]:
        assert self.dtype is not None, 'Box dtype cannot be None'
        if is_float_integer(high):
            bounded_above = np.full(self.shape, high, dtype=float) < np.inf

            if np.isnan(high):
                raise ValueError(f"No high value can be equal to `np.nan`, high={high}")
            elif np.isposinf(high):
                if self.dtype.kind == "i":  # signed int
                    high = dtype_max
                elif self.dtype.kind in {"u", "b"}:  # unsigned int
                    raise ValueError(
                        f"Box unsigned int dtype don't support `np.inf`, high={high}"
                    )
            elif high > dtype_max:
                raise ValueError(
                    f"Box high is out of bounds of the dtype range, high={high}, max dtype={dtype_max}"
                )

            high = np.full(self.shape, high, dtype=self.dtype)
            return high, bounded_above
        else:
            if not isinstance(high, np.ndarray):
                raise ValueError(
                    f"Box high must be a np.ndarray, integer, or float, actual type={type(high)}"
                )
            elif not (
                np.issubdtype(high.dtype, np.floating)
                or np.issubdtype(high.dtype, np.integer)
                or high.dtype == np.bool_
            ):
                raise ValueError(
                    f"Box high must be a floating or integer dtype, actual dtype={high.dtype}"
                )
            elif np.any(np.isnan(high)):
                raise ValueError(f"No high value can be equal to `np.nan`, high={high}")

            bounded_above = high < np.inf

            posinf = np.isposinf(high)
            if np.any(posinf):
                if self.dtype.kind == "i":  # signed int
                    high[posinf] = dtype_max
                elif self.dtype.kind in {"u", "b"}:  # unsigned int
                    raise ValueError(
                        f"Box unsigned int dtype don't support `np.inf`, high={high}"
                    )
            elif high.dtype != self.dtype and np.any(dtype_max < high):
                raise ValueError(
                    f"Box high is out of bounds of the dtype range, high={high}, max dtype={dtype_max}"
                )
            
            assert not np.issubdtype(self.dtype, np.void)
            if (
                np.issubdtype(high.dtype, np.floating)
                and np.issubdtype(self.dtype, np.floating)
                and np.finfo(self.dtype).precision < np.finfo(high.dtype).precision
            ):
                print(
                    f"Box high's precision lowered by casting to {self.dtype}, current high.dtype={high.dtype}"
                )
            
            return high.astype(self.dtype), bounded_above

    @property
    def shape(self) -> tuple[int, ...]:
        """Has stricter type than gym.Space - never None."""
        return self._shape

    def is_bounded(self, manner: str = "both") -> bool:
        below = bool(np.all(self.bounded_below))
        above = bool(np.all(self.bounded_above))
        if manner == "both":
            return below and above
        elif manner == "below":
            return below
        elif manner == "above":
            return above
        else:
            raise ValueError(
                f"manner is not in {{'below', 'above', 'both'}}, actual value: {manner}"
            )

    def sample(self, mask: None = None) -> NDArray[Any]:
        assert self.dtype is not None, 'Box dtype cannot be None'
        if mask is not None:
            raise ValueError(
                f"Box.sample cannot be provided a mask, actual value: {mask}"
            )

        high = self.high if self.dtype.kind == "f" else self.high.astype("int64") + 1
        sample = np.empty(self.shape)

        # Masking arrays which classify the coordinates according to interval type
        unbounded = ~self.bounded_below & ~self.bounded_above
        upp_bounded = ~self.bounded_below & self.bounded_above
        low_bounded = self.bounded_below & ~self.bounded_above
        bounded = self.bounded_below & self.bounded_above

        # Vectorized sampling by interval type
        sample[unbounded] = self.np_random.normal(size=unbounded[unbounded].shape)

        sample[low_bounded] = (
            self.np_random.exponential(size=low_bounded[low_bounded].shape)
            + self.low[low_bounded]
        )

        sample[upp_bounded] = (
            -self.np_random.exponential(size=upp_bounded[upp_bounded].shape)
            + high[upp_bounded]
        )

        sample[bounded] = self.np_random.uniform(
            low=self.low[bounded], high=high[bounded], size=bounded[bounded].shape
        )

        if self.dtype.kind in ["i", "u", "b"]:
            sample = np.floor(sample)

        # clip values that would underflow/overflow
        if np.issubdtype(self.dtype, np.signedinteger):
            dtype_min = np.iinfo(self.dtype).min + 2
            dtype_max = np.iinfo(self.dtype).max - 2
            sample = sample.clip(min=dtype_min, max=dtype_max)
        elif np.issubdtype(self.dtype, np.unsignedinteger):
            dtype_min = np.iinfo(self.dtype).min
            dtype_max = np.iinfo(self.dtype).max
            sample = sample.clip(min=dtype_min, max=dtype_max)

        sample = sample.astype(self.dtype)

        # float64 values have lower than integer precision near int64 min/max, so clip
        # again in case something has been cast to an out-of-bounds value
        if self.dtype == np.int64:
            sample = sample.clip(min=self.low, max=self.high)

        return sample

    def contains(self, x: Any) -> bool:
        if not isinstance(x, np.ndarray):
            #logger.warn("Casting input x to numpy array.")
            try:
                x = np.asarray(x, dtype=self.dtype)
            except (ValueError, TypeError):
                return False

        return bool(
            np.can_cast(x.dtype, self.dtype)
            and x.shape == self.shape
            and np.all(x >= self.low)
            and np.all(x <= self.high)
        )
    
    def __repr__(self) -> str:
        return f"Box({self.low_repr}, {self.high_repr}, {self.shape}, {self.dtype})"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Box)
            and (self.shape == other.shape)
            and (self.dtype == other.dtype)
            and np.allclose(self.low, other.low)
            and np.allclose(self.high, other.high)
        )

class Discrete(Space[np.int64]):
    r"""A space consisting of finitely many elements.

    This class represents a finite subset of integers, more specifically a set of the form :math:`\{ a, a+1, \dots, a+n-1 \}`.

    Example:
        >>> from gymnasium.spaces import Discrete
        >>> observation_space = Discrete(2, seed=42) # {0, 1}
        >>> observation_space.sample()
        np.int64(0)
        >>> observation_space = Discrete(3, start=-1, seed=42)  # {-1, 0, 1}
        >>> observation_space.sample()
        np.int64(-1)
    """
    def __init__(
            self, 
            n: int | np.integer[Any], 
            seed: int | np.random.Generator | None = None,
            start: int | np.integer[Any] = 0 
        ):
        assert np.issubdtype(type(n), np.integer), f"Expected integer type, actual type: {type(n)}"
        assert n > 0, "n (counts) have to be positive"
        assert np.issubdtype(type(start), np.integer), f"Expected integer type, actual type: {type(start)}"
        
        self.n = np.int64(n)
        self.start = np.int64(start)
        super().__init__((), np.int64, seed)
    
    def sample(self, mask: MaskNDArray | None = None) -> np.int64:
        if mask is not None:
            assert isinstance(mask, np.ndarray
            ), f"The expected type of the mask is np.ndarray, actual type: {type(mask)}"
            
            assert (mask.dtype == np.int8
            ), f"The expected dtype of the mask is np.int8, actual dtype: {mask.dtype}"
            
            assert mask.shape == (self.n,
            ), f"The expected shape of the mask is {(self.n,)}, actual shape: {mask.shape}"
            
            valid_action_mask = mask == 1
            
            assert np.all(np.logical_or(mask == 0, valid_action_mask)
            ), f"All values of a mask should be 0 or 1, actual values: {mask}"
            
            if np.any(valid_action_mask):
                return self.start + self.np_random.choice(np.where(valid_action_mask)[0])
            else:
                return self.start
            
        return np.int64(self.start + self.np_random.integers(self.n))
    
    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, int):
            as_int64 = np.int64(x)
        elif isinstance(x, (np.generic, np.ndarray)) and (
            np.issubdtype(x.dtype, np.integer) and x.shape == ()
        ):
            as_int64 = np.int64(x.item())
        else:
            return False

        return bool(self.start <= as_int64 < self.start + self.n)
    
    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        if self.start != 0:
            return f"Discrete({self.n}, start={self.start})"
        return f"Discrete({self.n})"

    def __eq__(self, other: Any) -> bool:
        """Check whether ``other`` is equivalent to this instance."""
        return (
            isinstance(other, Discrete)
            and self.n == other.n
            and self.start == other.start
        )

class MultiDiscrete(Space[NDArray[np.integer]]):
    """This represents the cartesian product of arbitrary :class:`Discrete` spaces.

    It is useful to represent game controllers or keyboards where each key can be represented as a discrete action space.

    Note:
        Some environment wrappers assume a value of 0 always represents the NOOP action.

    e.g. Nintendo Game Controller - Can be conceptualized as 3 discrete action spaces:

    1. Arrow Keys: Discrete 5  - NOOP[0], UP[1], RIGHT[2], DOWN[3], LEFT[4]  - params: min: 0, max: 4
    2. Button A:   Discrete 2  - NOOP[0], Pressed[1] - params: min: 0, max: 1
    3. Button B:   Discrete 2  - NOOP[0], Pressed[1] - params: min: 0, max: 1

    It can be initialized as ``MultiDiscrete([ 5, 2, 2 ])`` such that a sample might be ``array([3, 1, 0])``.

    Although this feature is rarely used, :class:`MultiDiscrete` spaces may also have several axes
    if ``nvec`` has several axes:

    Example:
        >>> from gymnasium.spaces import MultiDiscrete
        >>> import numpy as np
        >>> observation_space = MultiDiscrete(np.array([[1, 2], [3, 4]]), seed=42)
        >>> observation_space.sample()
        array([[0, 0],
               [2, 2]])
    """

    def __init__(
        self,
        nvec: NDArray[np.integer[Any]] | list[int],
        dtype: str | type[np.integer[Any]] = np.int64,
        seed: int | np.random.Generator | None = None,
        start: NDArray[np.integer[Any]] | list[int] | None = None,
    ):
        """Constructor of :class:`MultiDiscrete` space.

        The argument ``nvec`` will determine the number of values each categorical variable can take. If
        ``start`` is provided, it will define the minimal values corresponding to each categorical variable.

        Args:
            nvec: vector of counts of each categorical variable. This will usually be a list of integers. However,
                you may also pass a more complicated numpy array if you'd like the space to have several axes.
            dtype: This should be some kind of integer type.
            seed: Optionally, you can use this argument to seed the RNG that is used to sample from the space.
            start: Optionally, the starting value the element of each class will take (defaults to 0).
        """
        self.nvec = np.array(nvec, dtype=dtype, copy=True)
        if start is not None:
            self.start = np.array(start, dtype=dtype, copy=True)
        else:
            self.start = np.zeros(self.nvec.shape, dtype=dtype)

        assert (
            self.start.shape == self.nvec.shape
        ), "start and nvec (counts) should have the same shape"
        assert (self.nvec > 0).all(), "nvec (counts) have to be positive"

        super().__init__(self.nvec.shape, dtype, seed)

    @property
    def shape(self) -> tuple[int, ...]:
        """Has stricter type than :class:`gym.Space` - never None."""
        return self._shape  # type: ignore

    @property
    def is_np_flattenable(self):
        """Checks whether this space can be flattened to a :class:`spaces.Box`."""
        return True

    def sample(
        self, mask: tuple[MaskNDArray, ...] | None = None
    ) -> NDArray[np.integer[Any]]:
        """Generates a single random sample this space.

        Args:
            mask: An optional mask for multi-discrete, expects tuples with a ``np.ndarray`` mask in the position of each
                action with shape ``(n,)`` where ``n`` is the number of actions and ``dtype=np.int8``.
                Only ``mask values == 1`` are possible to sample unless all mask values for an action are ``0`` then the default action ``self.start`` (the smallest element) is sampled.

        Returns:
            An ``np.ndarray`` of :meth:`Space.shape`
        """
        if mask is not None:

            def _apply_mask(
                sub_mask: MaskNDArray | tuple[MaskNDArray, ...],
                sub_nvec: MaskNDArray | np.integer[Any],
                sub_start: MaskNDArray | np.integer[Any],
            ) -> int | list[Any]:
                if isinstance(sub_nvec, np.ndarray):
                    assert isinstance(
                        sub_mask, tuple
                    ), f"Expects the mask to be a tuple for sub_nvec ({sub_nvec}), actual type: {type(sub_mask)}"
                    assert len(sub_mask) == len(
                        sub_nvec
                    ), f"Expects the mask length to be equal to the number of actions, mask length: {len(sub_mask)}, nvec length: {len(sub_nvec)}"
                    return [
                        _apply_mask(new_mask, new_nvec, new_start)
                        for new_mask, new_nvec, new_start in zip(
                            sub_mask, sub_nvec, sub_start
                        )
                    ]
                else:
                    assert np.issubdtype(
                        type(sub_nvec), np.integer
                    ), f"Expects the sub_nvec to be an action, actually: {sub_nvec}, {type(sub_nvec)}"
                    assert isinstance(
                        sub_mask, np.ndarray
                    ), f"Expects the sub mask to be np.ndarray, actual type: {type(sub_mask)}"
                    assert (
                        len(sub_mask) == sub_nvec
                    ), f"Expects the mask length to be equal to the number of actions, mask length: {len(sub_mask)}, action: {sub_nvec}"
                    assert (
                        sub_mask.dtype == np.int8
                    ), f"Expects the mask dtype to be np.int8, actual dtype: {sub_mask.dtype}"

                    valid_action_mask = sub_mask == 1
                    assert np.all(
                        np.logical_or(sub_mask == 0, valid_action_mask)
                    ), f"Expects all masks values to 0 or 1, actual values: {sub_mask}"

                    if np.any(valid_action_mask):
                        return (
                            self.np_random.choice(np.where(valid_action_mask)[0])
                            + sub_start
                        )
                    else:
                        return sub_start

            return np.array(_apply_mask(mask, self.nvec, self.start), dtype=self.dtype)

        return (self.np_random.random(self.nvec.shape) * self.nvec).astype(
            self.dtype
        ) + self.start

    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, Sequence):
            x = np.array(x)  # Promote list to array for contains check

        # if nvec is uint32 and space dtype is uint32, then 0 <= x < self.nvec guarantees that x
        # is within correct bounds for space dtype (even though x does not have to be unsigned)
        return bool(
            isinstance(x, np.ndarray)
            and x.shape == self.shape
            and x.dtype != object
            and np.all(self.start <= x)
            and np.all(x - self.start < self.nvec)
        )

    def to_jsonable(
        self, sample_n: Sequence[NDArray[np.integer[Any]]]
    ) -> list[Sequence[int]]:
        """Convert a batch of samples from this space to a JSONable data type."""
        return [sample.tolist() for sample in sample_n]

    def from_jsonable(
        self, sample_n: list[Sequence[int]]
    ) -> list[NDArray[np.integer[Any]]]:
        """Convert a JSONable data type to a batch of samples from this space."""
        return [np.array(sample, dtype=np.int64) for sample in sample_n]

    def __repr__(self):
        """Gives a string representation of this space."""
        if np.any(self.start != 0):
            return f"MultiDiscrete({self.nvec}, start={self.start})"
        return f"MultiDiscrete({self.nvec})"

    def __getitem__(self, index: int | tuple[int, ...]):
        """Extract a subspace from this ``MultiDiscrete`` space."""
        nvec = self.nvec[index]
        start = self.start[index]
        if nvec.ndim == 0:
            subspace = Discrete(nvec, start=start)
        else:
            subspace = MultiDiscrete(nvec, self.dtype, start=start)

        # you don't need to deepcopy as np random generator call replaces the state not the data
        subspace.np_random.bit_generator.state = self.np_random.bit_generator.state

        return subspace

    def __len__(self):
        """Gives the ``len`` of samples from this space."""
        if self.nvec.ndim >= 2:
            print(
                "Getting the length of a multi-dimensional MultiDiscrete space."
            )
        return len(self.nvec)

    def __eq__(self, other: Any) -> bool:
        """Check whether ``other`` is equivalent to this instance."""
        return bool(
            isinstance(other, MultiDiscrete)
            and self.dtype == other.dtype
            and self.shape == other.shape
            and np.all(self.nvec == other.nvec)
            and np.all(self.start == other.start)
        )

    def __setstate__(self, state: Iterable[tuple[str, Any]] | Mapping[str, Any]):
        """Used when loading a pickled space.

        This method has to be implemented explicitly to allow for loading of legacy states.

        Args:
            state: The new state
        """
        state = dict(state)

        if "start" not in state:
            state["start"] = np.zeros(state["_shape"], dtype=state["dtype"])

        super().__setstate__(state)

class MultiBinary(Space[NDArray[np.int8]]):
    """An n-shape binary space.

    Elements of this space are binary arrays of a shape that is fixed during construction.

    Example:
        >>> from gymnasium.spaces import MultiBinary
        >>> observation_space = MultiBinary(5, seed=42)
        >>> observation_space.sample()
        array([1, 0, 1, 0, 1], dtype=int8)
        >>> observation_space = MultiBinary([3, 2], seed=42)
        >>> observation_space.sample()
        array([[1, 0],
               [1, 0],
               [1, 1]], dtype=int8)
    """

    def __init__(
        self,
        n: NDArray[np.integer[Any]] | Sequence[int] | int,
        seed: int | np.random.Generator | None = None,
    ):
        """Constructor of :class:`MultiBinary` space.

        Args:
            n: This will fix the shape of elements of the space. It can either be an integer (if the space is flat)
                or some sort of sequence (tuple, list or np.ndarray) if there are multiple axes.
            seed: Optionally, you can use this argument to seed the RNG that is used to sample from the space.
        """
        if isinstance(n, (Sequence, np.ndarray)):
            self.n = input_n = tuple(int(i) for i in n)
            assert (np.asarray(input_n) > 0).all()  # n (counts) have to be positive
        else:
            self.n = n = int(n)
            input_n = (n,)
            assert (np.asarray(input_n) > 0).all()  # n (counts) have to be positive

        super().__init__(input_n, np.int8, seed)

    @property
    def shape(self) -> tuple[int, ...]:
        """Has stricter type than gym.Space - never None."""
        return self._shape  # type: ignore

    @property
    def is_np_flattenable(self):
        """Checks whether this space can be flattened to a :class:`spaces.Box`."""
        return True

    def sample(self, mask: MaskNDArray | None = None) -> NDArray[np.int8]:
        """Generates a single random sample from this space.

        A sample is drawn by independent, fair coin tosses (one toss per binary variable of the space).

        Args:
            mask: An optional np.ndarray to mask samples with expected shape of ``space.shape``.
                For ``mask == 0`` then the samples will be ``0`` and ``mask == 1` then random samples will be generated.
                The expected mask shape is the space shape and mask dtype is ``np.int8``.

        Returns:
            Sampled values from space
        """
        if mask is not None:
            assert isinstance(
                mask, np.ndarray
            ), f"The expected type of the mask is np.ndarray, actual type: {type(mask)}"
            assert (
                mask.dtype == np.int8
            ), f"The expected dtype of the mask is np.int8, actual dtype: {mask.dtype}"
            assert (
                mask.shape == self.shape
            ), f"The expected shape of the mask is {self.shape}, actual shape: {mask.shape}"
            assert np.all(
                (mask == 0) | (mask == 1) | (mask == 2)
            ), f"All values of a mask should be 0, 1 or 2, actual values: {mask}"

            return np.where(
                mask == 2,
                self.np_random.integers(low=0, high=2, size=self.n, dtype=self.dtype),
                mask.astype(self.dtype),
            )

        return self.np_random.integers(low=0, high=2, size=self.n, dtype=self.dtype)

    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, Sequence):
            x = np.array(x)  # Promote list to array for contains check

        return bool(
            isinstance(x, np.ndarray)
            and self.shape == x.shape
            and np.all(np.logical_or(x == 0, x == 1))
        )

    def to_jsonable(self, sample_n: Sequence[NDArray[np.int8]]) -> list[Sequence[int]]:
        """Convert a batch of samples from this space to a JSONable data type."""
        return np.array(sample_n).tolist()

    def from_jsonable(self, sample_n: list[Sequence[int]]) -> list[NDArray[np.int8]]:
        """Convert a JSONable data type to a batch of samples from this space."""
        return [np.asarray(sample, self.dtype) for sample in sample_n]

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        return f"MultiBinary({self.n})"

    def __eq__(self, other: Any) -> bool:
        """Check whether `other` is equivalent to this instance."""
        return isinstance(other, MultiBinary) and self.n == other.n

class Tuple(Space[typing.Tuple[Any, ...]], typing.Sequence[Any]):
    """A tuple (more precisely: the cartesian product) of :class:`Space` instances.

    Elements of this space are tuples of elements of the constituent spaces.

    Example:
        >>> from gymnasium.spaces import Tuple, Box, Discrete
        >>> observation_space = Tuple((Discrete(2), Box(-1, 1, shape=(2,))), seed=42)
        >>> observation_space.sample()
        (np.int64(0), array([-0.3991573 ,  0.21649833], dtype=float32))
    """

    def __init__(
        self,
        spaces: Iterable[Space[Any]],
        seed: int | typing.Sequence[int] | np.random.Generator | None = None,
    ):
        r"""Constructor of :class:`Tuple` space.

        The generated instance will represent the cartesian product :math:`\text{spaces}[0] \times ... \times \text{spaces}[-1]`.

        Args:
            spaces (Iterable[Space]): The spaces that are involved in the cartesian product.
            seed: Optionally, you can use this argument to seed the RNGs of the ``spaces`` to ensure reproducible sampling.
        """
        self.spaces = tuple(spaces)
        for space in self.spaces:
            assert isinstance(
                space, Space
            ), f"{space} does not inherit from `gymnasium.Space`. Actual Type: {type(space)}"
        super().__init__(None, None, seed)  # type: ignore

    @property
    def is_np_flattenable(self):
        """Checks whether this space can be flattened to a :class:`spaces.Box`."""
        return all(space.is_np_flattenable for space in self.spaces)

    def seed(self, seed: int | tuple[int] | None = None) -> tuple[int, ...]:
        """Seed the PRNG of this space and all subspaces.

        Depending on the type of seed, the subspaces will be seeded differently

        * ``None`` - All the subspaces will use a random initial seed
        * ``Int`` - The integer is used to seed the :class:`Tuple` space that is used to generate seed values for each of the subspaces. Warning, this does not guarantee unique seeds for all the subspaces.
        * ``List`` - Values used to seed the subspaces. This allows the seeding of multiple composite subspaces ``[42, 54, ...]``.

        Args:
            seed: An optional list of ints or int to seed the (sub-)spaces.

        Returns:
            A tuple of the seed values for all subspaces
        """
        if seed is None:
            return tuple(space.seed(None) for space in self.spaces)
        elif isinstance(seed, int):
            super().seed(seed)
            subseeds = self.np_random.integers(
                np.iinfo(np.int32).max, size=len(self.spaces)
            )
            return tuple(
                subspace.seed(int(subseed))
                for subspace, subseed in zip(self.spaces, subseeds)
            )
        elif isinstance(seed, (tuple, list)):
            if len(seed) != len(self.spaces):
                raise ValueError(
                    f"Expects that the subspaces of seeds equals the number of subspaces. Actual length of seeds: {len(seed)}, length of subspaces: {len(self.spaces)}"
                )

            return tuple(
                space.seed(subseed) for subseed, space in zip(seed, self.spaces)
            )
        else:
            raise TypeError(
                f"Expected seed type: list, tuple, int or None, actual type: {type(seed)}"
            )

    def sample(self, mask: tuple[Any | None, ...] | None = None) -> tuple[Any, ...]:
        """Generates a single random sample inside this space.

        This method draws independent samples from the subspaces.

        Args:
            mask: An optional tuple of optional masks for each of the subspace's samples,
                expects the same number of masks as spaces

        Returns:
            Tuple of the subspace's samples
        """
        if mask is not None:
            assert isinstance(
                mask, tuple
            ), f"Expected type of mask is tuple, actual type: {type(mask)}"
            assert len(mask) == len(
                self.spaces
            ), f"Expected length of mask is {len(self.spaces)}, actual length: {len(mask)}"

            return tuple(
                space.sample(mask=sub_mask)
                for space, sub_mask in zip(self.spaces, mask)
            )

        return tuple(space.sample() for space in self.spaces)

    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, (list, np.ndarray)):
            x = tuple(x)  # Promote list and ndarray to tuple for contains check

        return (
            isinstance(x, tuple)
            and len(x) == len(self.spaces)
            and all(space.contains(part) for (space, part) in zip(self.spaces, x))
        )

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        return "Tuple(" + ", ".join([str(s) for s in self.spaces]) + ")"

    def to_jsonable(
        self, sample_n: typing.Sequence[tuple[Any, ...]]
    ) -> list[list[Any]]:
        """Convert a batch of samples from this space to a JSONable data type."""
        # serialize as list-repr of tuple of vectors
        return [
            space.to_jsonable([sample[i] for sample in sample_n])
            for i, space in enumerate(self.spaces)
        ]

    def from_jsonable(self, sample_n: list[list[Any]]) -> list[tuple[Any, ...]]:
        """Convert a JSONable data type to a batch of samples from this space."""
        return [
            sample
            for sample in zip(
                *[
                    space.from_jsonable(sample_n[i])
                    for i, space in enumerate(self.spaces)
                ]
            )
        ]

    def __getitem__(self, index: int) -> Space[Any]:
        """Get the subspace at specific `index`."""
        return self.spaces[index]

    def __len__(self) -> int:
        """Get the number of subspaces that are involved in the cartesian product."""
        return len(self.spaces)

    def __eq__(self, other: Any) -> bool:
        """Check whether ``other`` is equivalent to this instance."""
        return isinstance(other, Tuple) and self.spaces == other.spaces

class Dict(Space[typing.Dict[str, Any]], typing.Mapping[str, Space[Any]]):
    """A dictionary of :class:`Space` instances.

    Elements of this space are (ordered) dictionaries of elements from the constituent spaces.

    Example:
        >>> from gymnasium.spaces import Dict, Box, Discrete
        >>> observation_space = Dict({"position": Box(-1, 1, shape=(2,)), "color": Discrete(3)}, seed=42)
        >>> observation_space.sample()
        {'color': np.int64(0), 'position': array([-0.3991573 ,  0.21649833], dtype=float32)}

        With a nested dict:

        >>> from gymnasium.spaces import Box, Dict, Discrete, MultiBinary, MultiDiscrete
        >>> Dict(  # doctest: +SKIP
        ...     {
        ...         "ext_controller": MultiDiscrete([5, 2, 2]),
        ...         "inner_state": Dict(
        ...             {
        ...                 "charge": Discrete(100),
        ...                 "system_checks": MultiBinary(10),
        ...                 "job_status": Dict(
        ...                     {
        ...                         "task": Discrete(5),
        ...                         "progress": Box(low=0, high=100, shape=()),
        ...                     }
        ...                 ),
        ...             }
        ...         ),
        ...     }
        ... )

    It can be convenient to use :class:`Dict` spaces if you want to make complex observations or actions more human-readable.
    Usually, it will not be possible to use elements of this space directly in learning code. However, you can easily
    convert :class:`Dict` observations to flat arrays by using a :class:`gymnasium.wrappers.FlattenObservation` wrapper.
    Similar wrappers can be implemented to deal with :class:`Dict` actions.
    """

    def __init__(
        self,
        spaces: None | dict[str, Space] | Sequence[tuple[str, Space]] = None,
        seed: dict | int | np.random.Generator | None = None,
        **spaces_kwargs: Space,
    ):
        """Constructor of :class:`Dict` space.

        This space can be instantiated in one of two ways: Either you pass a dictionary
        of spaces to :meth:`__init__` via the ``spaces`` argument, or you pass the spaces as separate
        keyword arguments (where you will need to avoid the keys ``spaces`` and ``seed``)

        Args:
            spaces: A dictionary of spaces. This specifies the structure of the :class:`Dict` space
            seed: Optionally, you can use this argument to seed the RNGs of the spaces that make up the :class:`Dict` space.
            **spaces_kwargs: If ``spaces`` is ``None``, you need to pass the constituent spaces as keyword arguments, as described above.
        """
        # Convert the spaces into an OrderedDict
        if isinstance(spaces, collections.abc.Mapping):
            # for legacy reasons, we need to preserve the sorted dictionary items.
            # as this could matter for projects flatten the dictionary.
            try:
                spaces = dict(sorted(spaces.items()))
            except TypeError:
                # Incomparable types (e.g. `int` vs. `str`, or user-defined types) found.
                # The keys remain in the insertion order.
                spaces = dict(spaces.items())
        elif isinstance(spaces, Sequence):
            spaces = dict(spaces)
        elif spaces is None:
            spaces = dict()
        else:
            raise TypeError(
                f"Unexpected Dict space input, expecting dict, OrderedDict or Sequence, actual type: {type(spaces)}"
            )

        # Add kwargs to spaces to allow both dictionary and keywords to be used
        for key, space in spaces_kwargs.items():
            if key not in spaces:
                spaces[key] = space
            else:
                raise ValueError(
                    f"Dict space keyword '{key}' already exists in the spaces dictionary."
                )

        self.spaces: dict[str, Space[Any]] = spaces
        for key, space in self.spaces.items():
            assert isinstance(
                space, Space
            ), f"Dict space element is not an instance of Space: key='{key}', space={space}"

        # None for shape and dtype, since it'll require special handling
        super().__init__(None, None, seed)  # type: ignore

    @property
    def is_np_flattenable(self):
        """Checks whether this space can be flattened to a :class:`spaces.Box`."""
        return all(space.is_np_flattenable for space in self.spaces.values())

    def seed(self, seed: int | dict[str, Any] | None = None) -> dict[str, int]:
        """Seed the PRNG of this space and all subspaces.

        Depending on the type of seed, the subspaces will be seeded differently

        * ``None`` - All the subspaces will use a random initial seed
        * ``Int`` - The integer is used to seed the :class:`Dict` space that is used to generate seed values for each of the subspaces. Warning, this does not guarantee unique seeds for all subspaces, though is very unlikely.
        * ``Dict`` - A dictionary of seeds for each subspace, requires a seed key for every subspace. This supports seeding of multiple composite subspaces (``Dict["space": Dict[...], ...]`` with ``{"space": {...}, ...}``).

        Args:
            seed: An optional int or dictionary of subspace keys to int to seed each PRNG. See above for more details.

        Returns:
            A dictionary for the seed values of the subspaces
        """
        if seed is None:
            return {key: subspace.seed(None) for (key, subspace) in self.spaces.items()}
        elif isinstance(seed, int):
            super().seed(seed)
            # Using `np.int32` will mean that the same key occurring is extremely low, even for large subspaces
            subseeds = self.np_random.integers(
                np.iinfo(np.int32).max, size=len(self.spaces)
            )
            return {
                key: subspace.seed(int(subseed))
                for (key, subspace), subseed in zip(self.spaces.items(), subseeds)
            }
        elif isinstance(seed, dict):
            if seed.keys() != self.spaces.keys():
                raise ValueError(
                    f"The seed keys: {seed.keys()} are not identical to space keys: {self.spaces.keys()}"
                )

            return {key: self.spaces[key].seed(seed[key]) for key in seed.keys()}
        else:
            raise TypeError(
                f"Expected seed type: dict, int or None, actual type: {type(seed)}"
            )

    def sample(self, mask: dict[str, Any] | None = None) -> dict[str, Any]:
        """Generates a single random sample from this space.

        The sample is an ordered dictionary of independent samples from the constituent spaces.

        Args:
            mask: An optional mask for each of the subspaces, expects the same keys as the space

        Returns:
            A dictionary with the same key and sampled values from :attr:`self.spaces`
        """
        if mask is not None:
            assert isinstance(
                mask, dict
            ), f"Expects mask to be a dict, actual type: {type(mask)}"
            assert (
                mask.keys() == self.spaces.keys()
            ), f"Expect mask keys to be same as space keys, mask keys: {mask.keys()}, space keys: {self.spaces.keys()}"
            return {k: space.sample(mask=mask[k]) for k, space in self.spaces.items()}

        return {k: space.sample() for k, space in self.spaces.items()}

    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, dict) and x.keys() == self.spaces.keys():
            return all(x[key] in self.spaces[key] for key in self.spaces.keys())
        return False

    def __getitem__(self, key: str) -> Space[Any]:
        """Get the space that is associated to `key`."""
        return self.spaces[key]

    def keys(self) -> KeysView:
        """Returns the keys of the Dict."""
        return KeysView(self.spaces)

    def __setitem__(self, key: str, value: Space[Any]):
        """Set the space that is associated to `key`."""
        assert isinstance(
            value, Space
        ), f"Trying to set {key} to Dict space with value that is not a gymnasium space, actual type: {type(value)}"
        self.spaces[key] = value

    def __iter__(self):
        """Iterator through the keys of the subspaces."""
        yield from self.spaces

    def __len__(self) -> int:
        """Gives the number of simpler spaces that make up the `Dict` space."""
        return len(self.spaces)

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        return (
            "Dict(" + ", ".join([f"{k!r}: {s}" for k, s in self.spaces.items()]) + ")"
        )

    def __eq__(self, other: Any) -> bool:
        """Check whether `other` is equivalent to this instance."""
        return (
            isinstance(other, Dict)
            # Comparison of `OrderedDict`s is order-sensitive
            and self.spaces == other.spaces  # OrderedDict.__eq__
        )

