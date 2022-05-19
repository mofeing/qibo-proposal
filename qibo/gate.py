from typing import Any, Sequence
import abc
from typing_extensions import Self


class Gate:
    __slots__ = ("__qubits__",)

    def __init__(self, *qubits):
        super().__init__()

        if len(qubits) != self.nqubits:
            raise ValueError(f"number of qubits must be {self.nqubits}")

        self.__qubits__ = qubits

    @classmethod
    def new_type(cls, name: str, /, n: int = 1, *, params: Sequence[str] = None):
        attrs = {}
        if params:
            attrs = {
                "__parameters__": {param: None for param in params},
                # "__slots__": ("__parameters__",),
            }

        return type(name, (cls,), attrs, nqubits=n)

    @classmethod
    @property
    def nqubits(cls) -> int:
        return cls.__nqubits__

    @property
    def qubits(self) -> Sequence[int]:
        return self.__qubits__

    def __init_subclass__(cls, /, nqubits: int = None):
        super().__init_subclass__()

        if nqubits is None:
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


class Parametric(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subcls):
        if cls is not Parametric:
            return NotImplemented

        return hasattr(subcls, "__parameters__")

    __parameters__ = []


I = Gate.new_type("I")
X = Gate.new_type("X")
Y = Gate.new_type("Y")
Z = Gate.new_type("Z")

Rx = Gate.new_type("Rx", params=["theta"])
Ry = Gate.new_type("Ry", params=["theta"])
Rz = Gate.new_type("Rz", params=["theta"])

H = Gate.new_type("H")

S = Gate.new_type("S")
Sd = Gate.new_type("Sd")
T = Gate.new_type("T")
Td = Gate.new_type("Td")

Swap = Gate.new_type("Swap", n=2)
iSwap = Gate.new_type("iSwap", n=2)

Cx = Gate.new_type("Cx", n=2)
Cy = Gate.new_type("Cy", n=2)
Cz = Gate.new_type("Cz", n=2)
Control = Gate.new_type("Control", n=2, params=["U"])


class Pauli(metaclass=abc.ABCMeta):
    """Abstract Base Class for Pauli gates (I, X, Y, Z)."""


for cls in [I, X, Y, Z]:
    Pauli.register(cls)


class Clifford(metaclass=abc.ABCMeta):
    """Abstract Base Class for Clifford gates."""


for cls in [I, X, Y, Z, H, S, Cx]:
    Clifford.register(cls)


class Size:
    def __init__(self, n: int):
        self.n = n

    def __subclasscheck__(self, subcls: type) -> bool:
        return issubclass(subcls, Gate) and self.n == subcls.nqubits

    def __instancecheck__(self, instance: Any) -> bool:
        return issubclass(instance.__class__, self)
