from typing import Any, Sequence
import abc
from numbers import Number
import numpy as np


class Gate(abc.ABC):
    __slots__ = ("__qubits__",)

    def __init__(self, *qubits):
        super().__init__()

        if len(qubits) != self.nqubits:
            raise ValueError(f"{str(self.__class__)} is a {self.nqubits}-qubit(s) gate")

        self.__qubits__ = qubits

    @classmethod
    @property
    def nqubits(cls) -> int:
        return cls.__nqubits__

    @property
    def qubits(self) -> Sequence[int]:
        return self.__qubits__

    @abc.abstractproperty
    @property
    def dagger(cls) -> type:
        raise NotImplementedError()

    def __init_subclass__(cls, /, nqubits: int = None):
        super().__init_subclass__()

        nqubits = getattr(cls, "__nqubits__", nqubits)
        if nqubits is None or nqubits < 1:
            raise ValueError(f"{nqubits=} must a non-zero positive integer")

        cls.__nqubits__ = nqubits

    def __getattr__(self, attr: str):
        """Retrieve parameter if any."""
        if not isinstance(self, Parametric):
            raise AttributeError(f"{self.__class__} is not Parametric")

        try:
            return self.__parameters__[attr]
        except KeyError as err:
            raise AttributeError(str(err))


class Size:
    def __init__(self, n: int):
        self.n = n

    def __class_getitem__(cls, n: int):
        return type(
            f"Size[{n}]",
            (Size,),
            {
                "__nqubits__": n,
                "__init_subclass__": Size.__init_subclass__,
            },
        )

    def __subclasscheck__(self, subcls: type) -> bool:
        return issubclass(subcls, Gate) and self.n == subcls.nqubits

    def __instancecheck__(self, instance: Any) -> bool:
        return issubclass(instance.__class__, self)

    @staticmethod
    def of(cls: type) -> int:
        return Size(cls.__nqubits__)


class Parametric(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subcls):
        if cls is not Parametric:
            return NotImplemented

        return hasattr(subcls, "__parameters__") and isinstance(subcls, dict[str, Number])

    __parameters__: dict[str, Number] = dict()


class Hermitian(metaclass=abc.ABCMeta):
    """Abstract Base Class for Hermitian operators.

    If hermitian, then H = H†.
    """

    __hermitian__ = True

    @classmethod
    def __subclasshook__(cls, subcls):
        return hasattr(subcls, "__hermitian__") and subcls.__hermitian__

    @property
    def dagger(cls):
        return cls


class Clifford(metaclass=abc.ABCMeta):
    """Abstract Base Class for Clifford gates."""


class Pauli(Clifford, Hermitian, Size[1]):
    """Abstract Base Class for Pauli gates (I, X, Y, Z)."""


class Realizable(metaclass=abc.ABCMeta):
    """Abstract Base Class for physically realizable gates."""


class I(Pauli, Gate):
    pass


class X(Pauli, Gate):
    pass


class Y(Pauli, Gate):
    pass


class Z(Pauli, Gate):
    pass


class AxialRotation:
    def __class_getitem__(cls, angle: float):
        return type(
            f"{cls.__name__}[{angle}]",
            (cls,),
            {
                "__parameters__": dict(angle=angle),
            },
        )

    @classmethod
    @property
    def __hermitian__(cls):
        angle = cls.__parameters__["angle"]

        return np.isclose(np.remainder(angle, np.pi), 0.0)


class Rx(AxialRotation, Size[1], Gate):
    pass


class Ry(AxialRotation, Size[1], Gate):
    pass


class Rz(AxialRotation, Size[1], Gate):
    pass


class H(Hermitian, Size[1], Gate):
    pass


class S(Hermitian, Size[1], Gate):
    pass


class Sd(Size[1], Gate):
    pass


class T(Size[1], Gate):
    pass


class Td(Size[1], Gate):
    pass


class Swap(Size[2], Gate):
    pass


class iSwap(Size[2], Gate):
    pass


# class Control(Gate):
#     pass


# Swap = Gate.new_type("Swap", n=2)
# iSwap = Gate.new_type("iSwap", n=2)

# Cx = Gate.new_type("Cx", n=2)
# Cy = Gate.new_type("Cy", n=2)
# Cz = Gate.new_type("Cz", n=2)
# Control = Gate.new_type("Control", n=2, params=["U"])


# for cls in [I, X, Y, Z, H, S, Cx]:
#     Clifford.register(cls)
