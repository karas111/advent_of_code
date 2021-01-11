import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [[int(x) for x in line.strip().split("\t")] for line in f.readlines() if line]


def part_a(grid):
    diffs = [max(line) - min(line) for line in grid]
    return sum(diffs)


def part_b(grid):
    def find_divs(row):
        for idx, i in enumerate(row):
            for j in row[idx+1:]:
                if i % j == 0:
                    return i / j
                elif j % i == 0:
                    return j / i
        raise ValueError("Not found")

    divs = [find_divs(row) for row in grid]
    return sum(divs)


def main():
    grid = parse_input()
    logger.info(f"Res A {part_a(grid)}")
    logger.info(f"Res B {part_b(grid)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
