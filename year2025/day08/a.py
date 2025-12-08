import logging
import math
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "test1.txt"


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
    # can use Find Union for better performance
    # but still calculating distances is quadratic
    circuits_rep = {c: {c} for c in circuits}
    i = 0
    for _, (c1, c2) in distances:
        new_c = circuits_rep[c1] | circuits_rep[c2]
        for c in new_c:
            circuits_rep[c] = new_c

        i += 1
        if not part_b and i >= rounds:
            break
        if len(new_c) == len(circuits):
            return c1[0] * c2[0]
    sizes = []
    seen = set()
    for c in circuits:
        if c in seen:
            continue
        sizes.append(len(circuits_rep[c]))
        seen = seen | circuits_rep[c]
    return sorted(sizes)


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
