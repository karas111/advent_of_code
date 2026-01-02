import itertools
import logging
import math
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> set[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return set(map(lambda x: int(x.strip()), f.readlines()))


def can_split(numbers: set[int], group_number: int) -> int:
    total = sum(numbers)
    if total % group_number != 0:
        return False
    expected = total // group_number
    numbers = list(sorted(numbers, reverse=True))
    buckets = [0] * group_number

    def backtrack(idx: int) -> bool:
        if idx == len(numbers):
            return all(buckets[i] == expected for i in range(group_number))
        for i in range(group_number):
            if buckets[i] + numbers[idx] <= expected:
                buckets[i] += numbers[idx]
                if backtrack(idx + 1):
                    return True
                buckets[i] -= numbers[idx]
            if buckets[i] == 0:
                break
        return False

    return backtrack(0)


def find_best(numbers: set[int], group_number: int) -> int:
    totla_sum = sum(numbers)
    if totla_sum % group_number != 0:
        return False
    part_sum = sum(numbers) // group_number
    for i in range(1, len(numbers)):
        best_qe = float("inf")
        for chosen in itertools.combinations(numbers, i):
            if sum(chosen) != part_sum:
                continue
            other_numbers = numbers - set(chosen)
            if not can_split(other_numbers, group_number - 1):
                continue
            best_qe = min(best_qe, math.prod(chosen))
        if best_qe != float("inf"):
            return best_qe


def main():
    packages = read_input()
    logger.info("Res a: %s", find_best(packages, 3))
    logger.info("Res b: %s", find_best(packages, 4))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
