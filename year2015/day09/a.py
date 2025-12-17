import itertools
import logging
import os
import re
from collections import defaultdict

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Graph = dict[str, dict[str, int]]


def read_input() -> Graph:
    pattern = r"(\w+) to (\w+) = (\d+)"
    res = defaultdict(dict)
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            from_, to, distance = re.match(pattern, line.strip()).groups()
            res[from_][to] = res[to][from_] = int(distance)
    return res


def find_paths(graph: Graph) -> list[int]:
    res = []
    for path in itertools.permutations(graph):
        res.append(sum(graph[from_][to] for from_, to in zip(path, path[1:])))
    return res


def main():
    graph = read_input()
    paths = find_paths(graph)
    logger.info("Res a: %s", min(paths))
    logger.info("Res b: %s", max(paths))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
