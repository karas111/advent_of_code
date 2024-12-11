import logging
import os
from functools import cache

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(n) for n in f.readline().split()]


def count_stones(numbers: list[int], iter_n: int):

    @cache
    def _count_stones(n: int, iter_n: int) -> int:
        if iter_n == 0:
            return 1
        if n == 0:
            return _count_stones(1, iter_n - 1)
        n_str = str(n)
        l = len(n_str)
        if l % 2 == 0:
            return _count_stones(int(n_str[: l // 2]), iter_n - 1) + _count_stones(
                int(n_str[l // 2 :]), iter_n - 1
            )
        return _count_stones(n * 2024, iter_n - 1)

    return sum(_count_stones(n, iter_n) for n in numbers)


def main():
    numbers = read_input()
    with catchtime(logger):
        res = count_stones(numbers, 25)
        logger.info("Res A: %s", res)
        res = count_stones(numbers, 75)
        logger.info("Res B: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
