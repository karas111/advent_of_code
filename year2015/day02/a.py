import logging
import math
import os
from itertools import combinations

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[tuple]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [tuple(map(int, line.strip().split("x"))) for line in f]


def box_area(box: tuple) -> int:
    walls = [a * b for a, b in combinations(box, 2)]
    return sum(walls) * 2 + min(walls)


def ribbon(box: tuple):
    wrap = 2 * min(a + b for a, b in combinations(box, 2))
    return wrap + math.prod(box)


def main():
    boxes = read_input()
    res = [box_area(b) for b in boxes]
    logger.info("Result a %d", sum(res))
    res = [ribbon(b) for b in boxes]
    logger.info("Result b %d", sum(res))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
