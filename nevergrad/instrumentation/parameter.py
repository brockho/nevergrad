import numpy as np
# pylint: disable=unused-import
from .core3 import Parameter, ParametersDict  # noqa


class Array(Parameter):
    """Array variable of a given shape, on which several transforms can be applied.
    """

    def __init__(self, *dims: int) -> None:
        super().__init__()
        self._value: np.ndarray = np.zeros(dims)

    @property
    def value(self) -> np.ndarray:
        return self._value

    @value.setter
    def value(self, new_value: np.ndarray) -> None:
        if not isinstance(new_value, np.ndarray):
            raise TypeError(f"Received a {type(new_value)} in place of a np.ndarray")
        if self._value.shape != new_value.shape:
            raise ValueError(f"Cannot set array of shape {self._value.shape} with value of shape {new_value.shape}")
        self._value = new_value

    def with_std_data(self, data: np.ndarray, deterministic: bool = True) -> None:
        self._value = data.reshape(self.value.shape)

    def to_std_data(self) -> np.ndarray:
        return self._value.ravel()

    def spawn_child(self) -> "Array":
        child = Array(*self.value.shape)
        child._value = self.value
        child.parents_uids.append(self.uid)
        return child