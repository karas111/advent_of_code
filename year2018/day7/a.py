import copy
import logging
import os
import re
import time

from sortedcontainers import SortedSet
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_edge(line: str):
    return re.match(
        r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line
    ).groups()


def parse_graph():
    res = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f.readlines():
            if line:
                a, b = parse_edge(line.strip())
                res.setdefault(a, set())
                res.setdefault(b, set())
                res[b].add(a)
    return res


def reverse_graph(graph):
    rev_graph = {}
    for node, edges in graph.items():
        for node2 in edges:
            rev_graph.setdefault(node, set())
            rev_graph.setdefault(node2, set()).add(node)
    return rev_graph


def topological_sort(graph):
    queue = SortedSet([node for node, edges in graph.items() if len(edges) == 0])
    rev_graph = reverse_graph(graph)
    res = []
    while queue:
        node = queue.pop(0)
        res.append(node)
        for other_node in rev_graph[node]:
            graph[other_node].remove(node)
            if len(graph[other_node]) == 0:
                queue.add(other_node)
    return res


def topological_sort_b(graph, workers=5, additional_time=60):
    workers = {i: 0 for i in range(workers)}
    max_deps = {node: 0 for node in graph}
    queue = SortedSet([(0, node) for node, edges in graph.items() if len(edges) == 0])

    def find_worker():
        return min(workers.items(), key=lambda x: x[1])[0]

    def get_node_id(start_time):
        all_matching = sorted(
            [(a[1], idx) for idx, a in enumerate(queue) if a[0] <= start_time]
        )
        if all_matching:
            return all_matching[0][1]
        return 0

    rev_graph = reverse_graph(graph)

    while queue:
        worker_id = find_worker()
        start_time, node = queue.pop(get_node_id(workers[worker_id]))

        task_time = additional_time + ord(node) - 64

        end_time = max(workers[worker_id], start_time) + task_time
        workers[worker_id] = end_time
        for other_node in rev_graph[node]:
            graph[other_node].remove(node)
            max_deps[other_node] = max(max_deps[other_node], end_time)
            if len(graph[other_node]) == 0:
                queue.add((max_deps[other_node], other_node))
    return workers


def main():
    graph = parse_graph()
    res_a = topological_sort(copy.deepcopy(graph))
    logger.info(f"Res A {''.join(res_a)}")
    res_b = topological_sort_b(copy.deepcopy(graph))
    logger.info(f"Res B {max(res_b.values())}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
