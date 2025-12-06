import logging
import math
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip("\n") for line in f]


def solve(numbers) -> list[int]:
    res = []
    for x in range(0, len(numbers[0])):
        column_n = [numbers[y][x] for y in range(len(numbers) - 1)]
        column_n = map(int, column_n)
        if numbers[-1][x] == "+":
            res.append(sum(column_n))
        else:
            res.append(math.prod(column_n))
    return res


def solve_b(text: list[str]):
    last_line = text[-1]
    indexes = [i for i, c in enumerate(last_line) if c in "+*"]
    indexes.append(len(last_line) + 1)
    res = []
    current_number_col = 0
    while current_number_col < len(indexes) - 1:
        start, end = indexes[current_number_col], indexes[current_number_col + 1]
        to_operate = []
        for x in range(start, end - 1):
            number_col = []
            for y in range(len(text) - 1):
                number_col.append(text[y][x])
            number = int("".join(number_col))
            to_operate.append(number)
        if last_line[start] == "+":
            res.append(sum(to_operate))
        else:
            res.append(math.prod(to_operate))
        current_number_col += 1
    return res


def main():
    text = read_input()
    numbers = [line.split() for line in text]
    res = solve(numbers)
    logger.info("Result a %s", sum(res))
    res = solve_b(text)
    logger.info("Result b %s", sum(res))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
