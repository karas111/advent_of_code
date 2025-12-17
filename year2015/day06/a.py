import logging
import os
import re
from typing import Iterable

import catch_time
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> Iterable[tuple[str, Cords, Cords]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            match_ = re.match(r"(.*) (\d+),(\d+) through (\d+),(\d+)", line.strip())
            yield match_.groups()[0], tuple(map(int, match_.groups()[1:]))


ACTIONS_A = {
    "turn on": lambda _: True,
    "turn off": lambda _: False,
    "toggle": lambda x: not x,
}

ACTIONS_B = {
    "turn on": lambda x: x + 1,
    "turn off": lambda x: max(0, x - 1),
    "toggle": lambda x: x + 2,
}


def solve(input_, part_b):
    grid = [[False] * 1000 for _ in range(1000)]
    actions = ACTIONS_B if part_b else ACTIONS_A
    for action, (x0, y0, x1, y1) in input_:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                grid[y][x] = actions[action](grid[y][x])
    return sum(sum(row) for row in grid)


def main():
    input_ = read_input()
    logger.info("Res a: %d", solve(input_, False))
    input_ = read_input()
    logger.info("Res b: %d", solve(input_, True))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
