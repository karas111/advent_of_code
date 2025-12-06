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
    text_trans = map("".join, zip(*text))
    text_trans = "\n".join([l.strip() for l in text_trans])
    res = []
    for op_text in text_trans.split("\n\n"):
        numbers_txt = op_text.split("\n")
        numbers_int = [
            int(number) if number[-1].isdigit() else int(number[:-1])
            for number in numbers_txt
        ]
        if numbers_txt[0][-1] == "+":
            res.append(sum(numbers_int))
        else:
            res.append(math.prod(numbers_int))
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
