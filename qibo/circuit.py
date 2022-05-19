from functools import singledispatchmethod
from typing_extensions import Self
from qibo.gate import Gate
import networkx as nx
from uuid import uuid5


class Circuit:
    __slots__ = ("graph",)

    def __init__(self, nqubits: int):
        graph = nx.DiGraph()
        head = dict[int, str]()

        graph.add_nodes_from(((f"l{i}i", {"gate": None, "lane": i}) for i in range(nqubits)))

        self.graph = graph

    @property
    def nqubits(self) -> int:
        return self.__nqubits

    @property
    def layers(self) -> int:
        raise NotImplementedError()

    @property
    def dagger(self) -> Self:
        raise NotImplementedError()

    @singledispatchmethod
    def __iadd__(self, _):
        raise TypeError()

    @__iadd__.register
    def _(self, gate: Gate):
        raise NotImplementedError()

    @__iadd__.register
    def _(self, other: Self):
        if self.nqubits != other.nqubits:
            raise ValueError("#qubits must match")

        raise NotImplementedError()
