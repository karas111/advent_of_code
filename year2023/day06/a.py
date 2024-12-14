import logging
import math
import os
import re

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> tuple[list[int], list[int]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        time = list(map(int, re.findall(r"\d+", f.readline())))
        distance = list(map(int, re.findall(r"\d+", f.readline())))
        return time, distance


def solve(t: int, s: int) -> tuple[int, int]:
    # -x^2 + t*x - s > 0
    delta = t**2 - 4 * s
    x0 = (t - delta**0.5) / 2
    x1 = (t + delta**0.5) / 2
    return math.floor(x0 + 1), math.ceil(x1 - 1)


def main():
    time, distance = read_input()
    with catchtime(logger):
        roots = [solve(t, s) for t, s in zip(time, distance)]
        res = [max_x - min_x + 1 for min_x, max_x in roots]
        logger.info("Res A: %s", math.prod(res))

        time = int("".join(map(str, time)))
        distance = int("".join(map(str, distance)))
        min_x, max_x = solve(time, distance)
        logger.info("Res B: %s", max_x - min_x + 1)


if __name__ == "__main__":
    init_logging()
    main()
