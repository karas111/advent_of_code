import logging
from collections import namedtuple
import os
import time
import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip("\n") for line in f.readlines() if line]


MOVE_VEC = [
    np.array([1, 0]),  # EAST
    np.array([0, 1]),  # SOUTH
    np.array([-1, 0]),  # WEST
    np.array([0, -1]),  # NORT
]


def pos_in_grid(pos, grid):
    return 0 <= pos[0] <= len(grid[0]) and 0 <= pos[1] < len(grid)


def part_a(grid, x, y):
    pos = np.array([x, y])
    direction = 1  # south
    res = ""
    steps = 0
    while pos_in_grid(pos, grid):
        c = grid[pos[1]][pos[0]]
        if c in "-|":
            pass
        elif c == "+":
            for new_dir in (-1, 1):
                new_dir = (direction + new_dir) % 4
                new_pos = pos + MOVE_VEC[new_dir]
                if pos_in_grid(new_pos, grid) and grid[new_pos[1]][new_pos[0]] != " ":
                    direction = new_dir
                    break
        elif c == " ":
            return res, steps
        else:
            res += c
        pos = pos + MOVE_VEC[direction]
        steps += 1
    return res, steps


def main():
    grid = parse_input()
    x = grid[0].index("|")
    res_a, res_b = part_a(grid, x, 0)
    logger.info(f"Res A {res_a}")
    logger.info(f"Res A {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
