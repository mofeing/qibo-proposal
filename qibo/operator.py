class Operator:
    def __new__(cls, name: str, /, nqubits: int = 1, *, params: list[str] = None):
        # call to Operator(...) creates new class
        if cls is Operator:
            return type(name, (cls,), {"_nqubits": nqubits, "_params": params})

        # call from child
        elif issubclass(cls, Operator):
            # TODO fix
            if cls.params:
                # parametric class (e.g. Rx(theta))
                # generate new metaclass, descendent of Operator, that creates a final class
                def __Operator_parametric__new__(cls, *args, **kwargs):
                    print("hallo!")
                    return type(name, (cls,), {"_" + param: kwargs[param] for param in cls.params})  # same name

                return type(cls.name, (cls,), {"__new__": __Operator_parametric__new__} | {"__" + param: None for param in cls.params})
            else:
                # instantiate operator (calls __init__ afterwards)
                return super().__new__(cls)

        else:
            raise TypeError()

    def __init__(self, *args):
        self.__qubits = args

    @classmethod
    @property
    def name(cls) -> str:
        return str(cls.__name__)

    # @classmethod
    # @property
    # def alias(cls) -> tuple[str]:
    #     return cls._alias

    @property
    def qubits(self) -> tuple[int, ...]:
        return self.__qubits

    @classmethod
    @property
    def nqubits(cls) -> int | tuple[int, ...]:
        return cls._nqubits

    @classmethod
    @property
    def params(cls) -> tuple[str]:
        return cls._params

    def __getattr__(self, attr: str):
        if attr not in self.params:
            raise AttributeError()

        return getattr(self, "_" + attr)


I = Operator("I")
X = Operator("X")
Y = Operator("Y")
Z = Operator("Z")

Rx = Operator("Rx", params=["theta"])
Ry = Operator("Ry", params=["theta"])
Rz = Operator("Rz", params=["theta"])

H = Operator("H")

S = Operator("S")
Sd = Operator("Sd")
T = Operator("T")
Td = Operator("Td")

Swap = Operator("Swap", nqubits=2)
iSwap = Operator("iSwap", nqubits=2)

Cx = Operator("Cx", nqubits=2)
Cy = Operator("Cy", nqubits=2)
Cz = Operator("Cz", nqubits=2)
Control = Operator("Control", nqubits=2, params=["U"])
