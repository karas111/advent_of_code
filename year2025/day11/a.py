import logging
import math
import os
from collections import defaultdict

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> dict[str, set]:
    res = defaultdict(set)
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.strip()
            src, neighbours = line.split(": ")
            res[src].update(neighbours.split(" "))
    return res


def solve(graph: dict[str, set[str]], start="you", end="out") -> int:
    paths = {}

    def dfs(node: str):
        if node in paths:
            return
        if node == end:
            paths[node] = 1
            return
        for n in graph[node]:
            dfs(n)
        paths[node] = sum(paths[n] for n in graph[node])

    dfs(start)
    return paths[start]


def solve_b(graph: dict[str, set[str]]) -> int:
    paths = [
        ["svr", "dac", "fft", "out"],
        ["svr", "fft", "dac", "out"],
    ]
    res = 0
    for path in paths:
        res += math.prod(
            solve(graph, path[i], path[i + 1]) for i in range(len(path) - 1)
        )
    return res


def main():
    graph = read_input()
    res = solve(graph)
    logger.info("Result a %s", res)
    res = solve_b(graph)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
