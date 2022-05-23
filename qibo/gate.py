from typing import Any, Sequence
import abc
from numbers import Number
import numpy as np


class Gate:
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

    @classmethod
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
        return issubclass(subcls, Gate) and self.__nqubits__ == subcls.nqubits

    def __instancecheck__(self, instance: Any) -> bool:
        return issubclass(instance.__class__, self)


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

    @classmethod
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

    @classmethod
    @property
    def dagger(cls):
        return cls.__mro__[1][-cls.__parameters__["angle"]]


class Rx(AxialRotation, Size[1], Gate):
    pass


class Ry(AxialRotation, Size[1], Gate):
    pass


class Rz(AxialRotation, Size[1], Gate):
    pass


class H(Hermitian, Size[1], Gate):
    pass


class S(Clifford, Size[1], Gate):
    pass


class Sd(Size[1], Gate):
    pass


S.dagger = Sd
Sd.dagger = S


class T(Size[1], Gate):
    pass


class Td(Size[1], Gate):
    pass


T.dagger = Td
Td.dagger = T


class Swap(Hermitian, Size[2], Gate):
    pass


class iSwap(Size[2], Gate):
    pass


class Control(Size[2], Gate):
    def __class_getitem__(cls, u: type):
        assert issubclass(u, Gate)
        return type(
            f"Control[{u.__name__}]",
            (Control,),
            {
                "__u__": u,
            },
        )

    def __init__(self, control: int = None, target: int = None):
        control = (control,) if isinstance(control, int) else tuple(control)
        target = (target,) if isinstance(target, int) else tuple(target)

        self._control = control
        self._target = target

        super().__init__(*control, *target)

    @property
    def control(self) -> tuple[int, ...]:
        return self._control

    @property
    def target(self) -> tuple[int, ...]:
        return self._target

    @classmethod
    @property
    def __nqubits__(cls) -> int:
        return 2

    @classmethod
    @property
    def __hermitian__(cls) -> bool:
        return issubclass(cls.__u__, Hermitian)

    @classmethod
    @property
    def dagger(cls):
        return cls[cls.__u__.dagger]


Cx = Control[X]
Cy = Control[Y]
Cz = Control[Z]


Clifford.register(Cx)
