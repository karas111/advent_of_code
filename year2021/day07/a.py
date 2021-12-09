import logging
import os
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> List[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(x.strip()) for x in f.readline().strip().split(",")]


def find_alligment(numbers):
    median = numbers[len(numbers) // 2]
    return sum(abs(x - median) for x in numbers)


def fuel_cost(path_size):
    return (1 + path_size) * path_size // 2


def find_with_cost(numbers):
    best_fuel = -1
    for allingment in range(min(numbers), max(numbers) + 1):
        fuel = sum(fuel_cost(abs(x - allingment)) for x in numbers)
        if best_fuel < 0 or best_fuel > fuel:
            best_fuel = fuel
    return best_fuel


def main():
    numbers = sorted(read_input())
    res = find_alligment(numbers)
    logger.info(f"Res a {res}")
    res = find_with_cost(numbers)
    logger.info(f"Res b {res}")


if __name__ == "__main__":
    init_logging()
    main()
