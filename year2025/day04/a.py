import logging
import os
from collections import deque

import catch_time
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> set[Cords]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return {
            Cords(x, y)
            for y, line in enumerate(f.readlines())
            for x, c in enumerate(line.strip())
            if c == "@"
        }


NEIGHBOURS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
N_CORDS = [Cords(x, y) for x, y in NEIGHBOURS]


def solve(grid: set[Cords], stop_after_one: bool):
    to_check = deque(grid)
    removed = set()
    while to_check:
        node = to_check.popleft()
        if node in removed:
            continue
        count_n = 0
        for d_cords in N_CORDS:
            neighbour = node + d_cords
            if neighbour in grid and (stop_after_one or neighbour not in removed):
                count_n += 1
        if count_n < 4:
            removed.add(node)
            if stop_after_one:
                continue
            for d_cords in N_CORDS:
                n_node = node + d_cords
                if n_node in grid:
                    to_check.append(n_node)
    return len(removed)


def main():
    grid = read_input()
    res = solve(grid, True)
    logger.info("Result a %s", res)
    res = solve(grid, False)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
