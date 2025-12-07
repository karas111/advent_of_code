import logging
import os
from collections import defaultdict

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def solve(grid: list[str]) -> int:
    beams = {grid[0].index("S"): 1}
    res = 0
    for line in grid[1:]:
        splitters = {idx for idx, c in enumerate(line) if c == "^"}
        newbeams = defaultdict(lambda: 0)
        for beam, incoming_beams in beams.items():
            if beam in splitters:
                res += 1
                newbeams[beam - 1] += incoming_beams
                newbeams[beam + 1] += incoming_beams
            else:
                newbeams[beam] += incoming_beams
        beams = newbeams
    return res, sum(beams.values())


def main():
    grid = read_input()
    res_a, res_b = solve(grid)
    logger.info("Result a %s", res_a)
    logger.info("Result b %s", res_b)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
