import logging
import os
from functools import lru_cache
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> List[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(x.strip()) for x in f.readline().strip().split(",")]


@lru_cache
def count_per_fish(days):
    if days <= 0:
        return 1
    else:
        return count_per_fish(days - 7) + count_per_fish(days - 9)


def count_fish(numbers, days=80):
    return sum(count_per_fish(days - x) for x in numbers)


def main():
    numbers = read_input()
    res = count_fish(numbers)
    logger.info(f"Res a {res}")
    res = count_fish(numbers, days=256)
    logger.info(f"Res b {res}")


if __name__ == "__main__":
    init_logging()
    main()
