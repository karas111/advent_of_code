import logging
import os
import re
from collections import deque
from dataclasses import dataclass
from queue import PriorityQueue
from typing import Iterable, TypeVar

from custom_collections.priority import PriorityEntry
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Node = TypeVar("Node")

Graph = dict[Node, set[Node]]
WeightedGraph = dict[Node, dict[Node, int]]
FlowRates = dict[Node, int]


def read_graph() -> tuple[FlowRates, Graph]:
    graph = {}
    flow_rates = {}
    pattern = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    )
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            m = pattern.match(line.strip())
            valve = m.group(1)
            flow = int(m.group(2))
            tunnels = {x.strip() for x in m.group(3).split(",")}
            graph[valve] = tunnels
            flow_rates[valve] = flow
    return flow_rates, graph


def bfs(start: str, graph: Graph) -> dict[str, int]:
    queue = deque([(start, 0)])
    res = {}
    while queue:
        current, l = queue.popleft()
        if current in res:
            continue
        res[current] = l
        for n in graph[current]:
            queue.append((n, l + 1))
    return res


def reduce_graph(
    flow_rates: FlowRates, graph: Graph
) -> tuple[WeightedGraph, dict[str, int]]:
    nodes_to_include = [
        node for node, rate in flow_rates.items() if rate > 0 or node == "AA"
    ]

    shortest = dict()
    for node in nodes_to_include:
        shortest[node] = {
            k: v for k, v in bfs(node, graph).items() if k in nodes_to_include
        }

    nodes_mapping = {node_str: 1 << i for i, node_str in enumerate(shortest)}
    shortest = {
        nodes_mapping[n]: {nodes_mapping[x]: dist for x, dist in neihbours.items()}
        for n, neihbours in shortest.items()
    }
    logger.info(nodes_mapping)
    logger.info(shortest)
    return shortest, nodes_mapping


@dataclass
class State:
    current: int
    remaining_time: int
    open_mask: int

    def __hash__(self):
        return hash((self.current, self.remaining_time, self.open_mask))

    # helper fields
    # all_valves_open_flow: int

    def is_open(self):
        return self.open_mask & self.current

    def get_neighbours(
        self, graph: WeightedGraph, flow_rates: FlowRates
    ) -> Iterable[tuple["State", int]]:
        total_possible_flow = sum(flow_rates.values())
        if self.remaining_time <= 0:
            return
        open_valves_flow = sum(
            rate for node, rate in flow_rates.items() if node & self.open_mask
        )
        if not self.is_open():
            yield (
                State(
                    self.current, self.remaining_time - 1, self.open_mask | self.current
                ),
                total_possible_flow - open_valves_flow,
            )
        for neighbour, dist in graph[self.current].items():
            if dist > self.remaining_time:
                continue
            yield (
                State(neighbour, self.remaining_time - dist, self.open_mask),
                (total_possible_flow - open_valves_flow) * dist,
            )
        # do noting state, no need, there is self<->self edge
        # yield (
        #     State(self.current, 0, self.open_mask),
        #     total_possible_flow - open_valves_flow * open_valves_flow,
        # )


def dijkstra(
    graph: WeightedGraph, start: State, flow_rates: FlowRates
) -> tuple[int, int]:
    frontier = PriorityQueue()
    frontier.put(PriorityEntry(0, start))
    cost_so_far = {start: 0}

    while not frontier.empty():
        state: State = frontier.get().data
        if state.remaining_time == 0:
            return cost_so_far[state], state.open_mask

        for n, edge_w in state.get_neighbours(graph, flow_rates):
            new_cost = cost_so_far[state] + edge_w
            if n not in cost_so_far or cost_so_far[n] > new_cost:
                cost_so_far[n] = new_cost
                frontier.put(PriorityEntry(new_cost, n))


def main():
    flow_rates, graph = read_graph()
    reduced_graph, mapping = reduce_graph(flow_rates, graph)
    flow_rates = {mapping[n]: v for n, v in flow_rates.items() if v or n == "AA"}
    logger.info("\n%s\n%s\n%s", mapping, flow_rates, reduced_graph)
    res, open_valves = dijkstra(reduced_graph, State(mapping["AA"], 30, 0), flow_rates)
    logger.info("Result a %s", 30 * sum(flow_rates.values()) - res)


if __name__ == "__main__":
    init_logging()
    main()
