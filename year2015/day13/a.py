import logging
import os
import re
from collections import defaultdict
from itertools import permutations

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> dict[str, dict[str]]:
    pattern = r"(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)."
    res = defaultdict(dict)
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            from_, lose_gain, n, to = re.match(pattern, line.strip()).groups()
            n = int(n) * (1 if lose_gain == "gain" else -1)
            res[from_][to] = n
    return res


def count_happines(order: list[str], graph: dict[str, dict[str]]) -> int:
    res = 0
    l = len(order)
    for i in range(l):
        res += graph[order[i]][order[(i + 1) % l]] + graph[order[(i + 1) % l]][order[i]]
    return res


def find_best_seating(graph: dict[str, dict[str]]) -> int:
    people = list(graph.keys())
    first = people.pop()
    return max(
        count_happines(order + (first,), graph) for order in permutations(people)
    )


def main():
    graph = read_input()
    logger.info("Res a: %d", find_best_seating(graph))

    for k in list(graph):
        graph["me"][k] = 0
        graph[k]["me"] = 0
    logger.info("Res b: %d", find_best_seating(graph))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
