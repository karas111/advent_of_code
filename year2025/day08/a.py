import logging
import math
import os

import catch_time
from custom_collections.findunion import FindUnion
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def solve(circuits, part_b=False):
    rounds = 1000 if INPUT_FILE == "input.txt" else 10
    distances = []
    for idx, c1 in enumerate(circuits[:-1]):
        for c2 in circuits[idx + 1 :]:
            dist = sum((a - b) ** 2 for a, b in zip(c1, c2))
            distances.append((dist, (c1, c2)))
    distances.sort()

    fu = FindUnion(circuits)
    i = 0
    for _, (c1, c2) in distances:
        fu.union(c1, c2)
        i += 1
        if not part_b and i >= rounds:
            break
        if part_b and fu.n_sets == 1:
            return c1[0] * c2[0]
    return sorted(map(len, fu.get_sets()))


def main():
    boxes = read_input()
    circuits = solve(boxes, part_b=False)
    logger.info("Result a %s", math.prod(circuits[-3:]))
    res = solve(boxes, part_b=True)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
