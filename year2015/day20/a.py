import logging

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def build_table(max_size=10**6, max_per_elf: int = 10**6):
    res = [1] * (max_size + 1)
    for i in range(2, max_size + 1):
        cur = i
        while cur <= max_size and cur // i <= max_per_elf:
            res[cur] += i
            cur += i
    return res


def solve_a(n: int) -> int:
    t = build_table()
    for idx, val in enumerate(t):
        if val * 10 >= n:
            return idx


def solve_b(n: int) -> int:
    t = build_table(max_per_elf=50)
    for idx, val in enumerate(t):
        if val * 11 >= n:
            return idx


def main():
    n = 33100000
    logger.info("Res a: %s", solve_a(n))
    logger.info("Res b: %s", solve_b(n))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
