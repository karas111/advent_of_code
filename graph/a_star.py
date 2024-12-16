import abc
from collections import defaultdict
from numbers import Number
from queue import PriorityQueue
from typing import Callable, DefaultDict, Iterable, Optional, Protocol, TypeVar, Union

from custom_collections.priority import PriorityEntry

Node = TypeVar("Node")


class Graph(Protocol[Node]):

    @abc.abstractmethod
    def neighbours(self, n: Node) -> Iterable[tuple[Node, Number]]: ...


def _reconstruct_path(node: Node, came_from: dict[Node, set[Node]]) -> tuple[Node, ...]:
    path = []
    while node is not None:
        path.append(node)
        if came_from[node]:
            node = came_from[node].pop()
        else:
            node = None
    return tuple(path[::-1])


def search_shortest(
    source: Node, goal: Node, graph: Graph, heurestic: Optional[Callable[[Node, Node], Number]] = None, reconstruct_path: bool = True
) -> tuple[Number, Union[list[Node]], dict[Node, set[Node]]]:
    if heurestic is None:
        def _heurestic(n1: Node, n2: Node) -> int:
            return 0
        heurestic = _heurestic
    cost_so_far: dict[Node, Number] = {source: 0}
    came_from: DefaultDict[Node, set[Node]] = defaultdict(set, {source: set()})
    frontier = PriorityQueue()
    frontier.put(PriorityEntry(0, source))

    while not frontier.empty():
        current: Node = frontier.get().data
        if current == goal:
            if reconstruct_path:
                return cost_so_far[goal], _reconstruct_path(goal, came_from)
            else:
                return cost_so_far[goal], came_from

        for neighbour, edge_w in graph.neighbours(current):
            new_cost = cost_so_far[current] + edge_w
            if neighbour not in cost_so_far or cost_so_far[neighbour] > new_cost:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + heurestic(neighbour, goal)
                frontier.put(PriorityEntry(priority, neighbour))
                # came_from[neighbour] = current
            if cost_so_far[neighbour] == new_cost:
                came_from[neighbour].add(current)
    raise ValueError("Not found path")
