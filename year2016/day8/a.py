import logging
import os
import re
import time
import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

PARSE_PATTERNS = {
    "row": r"rotate row y=(\d+) by (\d+)",
    "column": r"rotate column x=(\d+) by (\d+)",
    "rect": r"rect (\d+)x(\d+)",
}


def parse_input():
    def parse_inst(line):
        for inst, pattern in PARSE_PATTERNS.items():
            if inst in line:
                args = [int(x) for x in re.match(pattern, line).groups()]
                return inst, args

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_inst(line.strip()) for line in f.readlines() if line]


def paint(insts):
    grid = np.zeros((6, 50))
    # grid = np.zeros((3, 7))
    for inst, (arg1, arg2) in insts:
        if inst == "rect":
            grid[:arg2, :arg1].fill(1)
        elif inst == "row":
            grid[arg1] = np.roll(grid[arg1], arg2)
        elif inst == "column":
            grid[:, arg1] = np.roll(grid[:, arg1], arg2)
    return grid


def main():
    insts = parse_input()
    grid = paint(insts)
    logger.info(f"Res A {np.sum(grid)}")
    display = "\n".join(["".join(x and "#" or " " for x in line) for line in grid])
    logger.info(f"\n{display}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
