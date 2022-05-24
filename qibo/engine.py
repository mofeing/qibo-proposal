import abc
from typing import final
from qibo.gate import Gate
import pkg_resources


class Engine(abc.ABC):
    @abc.abstractmethod
    def apply_gate(self, gate: Gate):
        pass

    @final
    def __iadd__(self, gate: Gate):
        self.apply_gate(gate)
        return self

    @abc.abstractmethod
    def measure(self, qubit: int):
        """Measures a qubit.

        To keep consistency between physical realizations and software simulations, this method mutates the simulator instance.
        """
        pass


DEFAULT_BACKEND = "numpy"


class Simulator(Engine):
    """Classical software simulator."""

    ...


class StateVector:
    pass


class MPS:
    pass


class PEPS:
    pass


engines = {}
for entrypoint in pkg_resources.iter_entry_points("qibo_engines"):
    engines[entrypoint.name] = entrypoint.load()
