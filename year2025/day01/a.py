import logging
import os
import re

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            n = int(line.strip()[1:])
            n *= -1 if line[0] == "L" else 1
            res.append(n)
        return res


def simulate(numbers, any_click):
    current = 50
    res = 0

    for n in numbers:
        new_current = (current + n) % 100
        if any_click:
            res += abs(n) // 100
            is_left = n < 0
            n = n % 100
            n -= 100 if is_left else 0
            if current != 0:
                if n < 0:
                    res += (current + n) <= 0
                else:
                    res += (current + n) >= 100
        else:
            res += current == 0
        current = new_current
    return res


def main():
    numbers = read_input()
    res = simulate(numbers, False)
    logger.info("Result a %d", res)

    res = simulate(numbers, True)
    logger.info("Result b %d", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
