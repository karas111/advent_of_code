from collections import defaultdict
import logging
import os
from typing import Dict, List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Graph = Dict[str, List[str]]


def read_input() -> Graph:
    graph = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n1, n2 = line.split("-")
            graph.setdefault(n1, []).append(n2)
            graph.setdefault(n2, []).append(n1)
    return graph


def is_visited(node: str, visited: Dict[str, int], have_time: bool) -> bool:
    if node.isupper():
        return False
    if node in ["start", "end"]:
        return visited[node] > 0
    if have_time:
        return visited[node] > 1
    return visited[node] > 0


def bfs(
    graph: Graph,
    node: str = "start",
    visited: Dict[str, int] = None,
    current_path: List[str] = None,
    part_b: bool = False,
    have_time: bool = False,
) -> List[List[str]]:
    visited = visited or defaultdict(lambda: 0)
    current_path = current_path or []
    res = set()
    if is_visited(node, visited, have_time):
        return []
    if node.islower():
        visited[node] += 1
    if part_b:
        have_time = have_time and visited[node] < 2
    current_path.append(node)
    if node == "end":
        res.add(tuple(current_path))
    else:
        for neighbour in graph[node]:
            res.update(
                bfs(
                    graph,
                    node=neighbour,
                    visited=visited,
                    current_path=current_path,
                    have_time=have_time,
                    part_b=part_b,
                )
            )
    if node.islower():
        if part_b:
            have_time = visited[node] == 2
        visited[node] -= 1
    current_path.pop()
    return res


def main():
    graph = read_input()
    res = bfs(graph)
    logger.info(f"Res a {len(res)}")
    res = bfs(graph, part_b=True, have_time=True)
    logger.info(f"Res b {len(res)}")


if __name__ == "__main__":
    init_logging()
    main()
