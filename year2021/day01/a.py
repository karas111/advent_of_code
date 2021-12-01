import os
import logging

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_numbers():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = [int(line) for line in f if line]
    return res


def find_inc(numbers):
    res = 0
    for x, y in zip(numbers, numbers[1:]):
        if x < y:
            res += 1
    return res


def mean_numbers(numbers):
    return [sum(numbers[i: i + 3]) for i in range(len(numbers) - 2)]


def main():
    numbers = read_numbers()
    res = find_inc(numbers)
    logger.info(f"Result a {res}")
    numbers = mean_numbers(numbers)
    res = find_inc(numbers)
    logger.info(f"Result b {res}")


if __name__ == "__main__":
    init_logging()
    main()
