from functools import singledispatchmethod
from qibo.gate import Gate
import networkx as nx
from uuid import uuid4
import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Circuit:
    __slots__ = ("graph", "__nqubits")

    def __init__(self, nqubits: int):
        graph = nx.DiGraph()
        head = dict[int, str]()

        graph.add_nodes_from(((f"l{i}{t}", {"gate": None, "lane": i}) for i in range(nqubits) for t in ["i", "o"]))

        graph.add_edges_from(((f"l{i}i", f"l{i}o", {"lane": i}) for i in range(nqubits)))

        self.graph = graph
        self.__nqubits = nqubits

    @property
    def nqubits(self) -> int:
        return self.__nqubits

    @property
    def dagger(self) -> Self:
        raise NotImplementedError()

    @singledispatchmethod
    def __iadd__(self, _):
        return NotImplemented

    @__iadd__.register
    def add_gate(self, gate: Gate):
        assert all(i in range(self.nqubits) for i in gate.qubits)

        # create new node for gate
        new = str(uuid4())
        self.graph.add_node(new, gate=gate, lane=gate.qubits)

        # connect new node in between output node and its predecessor (last gate in lane)
        for lane in gate.qubits:
            out = f"l{lane}o"
            last = next(self.graph.predecessors(out))
            self.graph.remove_edge(last, out)
            self.graph.add_edge(last, new, lane=lane)
            self.graph.add_edge(new, out, lane=lane)


@Circuit.__iadd__.register(Circuit)
def _(self, other: Self):
    if self.nqubits != other.nqubits:
        raise ValueError("#qubits must match")

    raise NotImplementedError()
