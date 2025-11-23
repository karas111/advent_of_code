import logging
import os
import re
from collections import deque
from typing import TypeVar

from catch_time import catchtime
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
    return shortest


def encode_graph(graph: WeightedGraph, flow_rates: FlowRates):
    mapping = {node_str: 1 << i for i, node_str in enumerate(graph)}
    encoded_graph = {
        mapping[n]: {mapping[nn]: v for nn, v in neighbours.items()}
        for n, neighbours in graph.items()
    }
    flow_rates = {mapping[n]: flow_rates[n] for n in graph}
    return encoded_graph, flow_rates, mapping["AA"]


def visit(graph: WeightedGraph, flow_rates: FlowRates, start: int, minutes: int) -> int:
    answer = {}

    def visit_(
        current: int, open_mask: int, released_pessure: int, remaining_time: int
    ):
        answer[open_mask] = max(answer.get(open_mask, 0), released_pessure)
        for node, flow_rate in flow_rates.items():
            if not flow_rate:
                continue
            new_remaining_time = remaining_time - graph[current][node] - 1
            if node & open_mask or new_remaining_time <= 0:
                continue
            visit_(
                node,
                open_mask | node,
                released_pessure + new_remaining_time * flow_rate,
                new_remaining_time,
            )

    visit_(start, 0, 0, minutes)
    return answer


def main():
    flow_rates, graph = read_graph()
    graph = reduce_graph(flow_rates, graph)
    graph, flow_rates, start = encode_graph(graph, flow_rates)
    res = visit(graph, flow_rates, start, 30)
    logger.info("Result a %d", max(res.values()))

    visited = visit(graph, flow_rates, start, 26)
    res2 = max(
        a + b
        for a_mask, a in visited.items()
        for b_mask, b in visited.items()
        if not (a_mask & b_mask)
    )
    logger.info("Result b %d", res2)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
