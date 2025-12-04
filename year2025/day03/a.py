import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[list[int]]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            res.append(list(map(int, line.strip())))
        return res


def solve(banks: list[list[int]], digits: int) -> list[int]:
    def solve_bank(bank: list[int], digits: int = 12, n: int = 0) -> int:
        if digits == 0:
            return n
        # find biggest number without the last digits-1
        max_ = max(bank[: len(bank) - digits + 1])
        # get the idx of the biggest digit
        idx = bank.index(max_)
        n = 10 ** (digits - 1) * max_ + n
        # recurseviely find the rest
        return solve_bank(bank[idx + 1 :], digits - 1, n)

    return [solve_bank(bank, digits) for bank in banks]


def main():
    banks = read_input()
    maxes = solve(banks, digits=2)
    logger.info("Result a %d", sum(maxes))
    maxes = solve(banks, digits=12)
    logger.info("Result b %d", sum(maxes))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
