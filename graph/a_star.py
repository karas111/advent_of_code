import abc
from numbers import Number
from queue import PriorityQueue
from typing import Callable, Iterable, Optional, Protocol, TypeVar

from custom_collections.priority import PriorityEntry

Node = TypeVar("Node")


class Graph(Protocol[Node]):

    @abc.abstractmethod
    def neighbours(self, n: Node) -> Iterable[tuple[Node, Number]]: ...


def _reconstruct_path(node: Node, came_from: dict[Node, Optional[Node]]) -> list[Node]:
    path = []
    while node is not None:
        path.append(node)
        node = came_from[node]
    return path[::-1]


def search_shortest(
    source: Node, goal: Node, graph: Graph, heurestic: Optional[Callable[[Node, Node], Number]] = None
) -> tuple[Number, list[Node]]:
    if heurestic is None:
        def _heurestic(n1: Node, n2: Node) -> int:
            return 0
        heurestic = _heurestic
    cost_so_far: dict[Node, Number] = {source: 0}
    came_from: dict[Node, Optional[Node]] = {source: None}
    frontier = PriorityQueue()
    frontier.put(PriorityEntry(0, source))

    while not frontier.empty():
        current: Node = frontier.get().data
        if current == goal:
            return cost_so_far[goal], _reconstruct_path(goal, came_from)

        for neighbour, edge_w in graph.neighbours(current):
            new_cost = cost_so_far[current] + edge_w
            if neighbour not in cost_so_far or cost_so_far[neighbour] > new_cost:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + heurestic(neighbour, goal)
                frontier.put(PriorityEntry(priority, neighbour))
                came_from[neighbour] = current
    raise ValueError("Not found path")
