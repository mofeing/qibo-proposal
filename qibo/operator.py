from numbers import Number
from typing import Optional, TypeVar


T = TypeVar("T")


def Const(obj: T) -> T:
    def getter(_):
        return obj

    if hasattr(obj, "__del__"):

        def deletter(o):
            o.__del__()

    else:
        deletter = None

    return property(fget=getter, fset=None, fdel=deletter)


class Operator(object):
    __parametric__: bool = False
    __parameters__: Optional[dict[str, Number]] = None

    def __new__(cls, *args, params=None, **kwargs):
        if cls.__parametric__:
            # shortcut
            if params:
                return super().__new__(cls, **kwargs)

            # TODO
            # e.g. Rx(3, theta=π/4)

            # e.g. Rotation on X-axis acting on qubit 4:
            #   gate = Rx(π/4)
            #   circ += gate(4)
            assert len(args) == len(cls.__parameters__), "must only provide parameters"
            params = {paramname: value for paramname, value in zip(cls.__parameters__.keys(), args)}

            return lambda *qubits: cls(*qubits, params=params, **kwargs)
        else:
            return super().__new__(cls, **kwargs)

    def __init_subclass__(cls, parameters: Optional[list[str]] = None, **kwargs):
        super().__init_subclass__(**kwargs)

        if parameters:
            cls.__parametric__ = True
            cls.__parameters__ = {param: None for param in parameters}

    def __init__(self, *qubits, params=None, **kwargs):
        if len(qubits) != self.n:
            raise ValueError(f"must provide {self.n} qubit indices only")

        self._qubits = qubits

        if self.__parametric__:
            assert set(self.__parameters__.keys()) == set(params.keys()), "must only provide parameters"

            self.__parameters__ |= params

    @classmethod
    def new_type(cls, name: str, /, n: int = 1, *, params: list[str] = None):
        if params:
            return type(name, (cls,), {"n": Const(n)}, parameters=params)
        else:
            return type(name, (cls,), {"n": Const(n)})

    def __len__(cls):
        return cls.n

    @classmethod
    def isparametric(cls) -> bool:
        return cls.__parametric__

    def params(self) -> Optional[dict[str, Number]]:
        return self.__parameters__

    def __getattr__(self, attr: str):
        """Retrieve parameter if any."""
        if not self.__parametric__:
            raise AttributeError(f"no parameters")

        attr_value = self.__parameters__.get(attr, False)
        if attr_value:
            return attr_value

        raise AttributeError(f"{attr} not found")


I = Operator.new_type("I")
X = Operator.new_type("X")
Y = Operator.new_type("Y")
Z = Operator.new_type("Z")

Rx = Operator.new_type("Rx", params=["theta"])
Ry = Operator.new_type("Ry", params=["theta"])
Rz = Operator.new_type("Rz", params=["theta"])

H = Operator.new_type("H")

S = Operator.new_type("S")
Sd = Operator.new_type("Sd")
T = Operator.new_type("T")
Td = Operator.new_type("Td")

Swap = Operator.new_type("Swap", n=2)
iSwap = Operator.new_type("iSwap", n=2)

Cx = Operator.new_type("Cx", n=2)
Cy = Operator.new_type("Cy", n=2)
Cz = Operator.new_type("Cz", n=2)
Control = Operator.new_type("Control", n=2, params=["U"])
