import logging
import os
import re
from collections import defaultdict

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Grid = list[str]


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def count_numbers(grid: Grid):
    max_y, max_x = len(grid), len(grid[0])
    numbers_connected = []
    star_numbers = defaultdict(list)
    number_pattern = re.compile(r"\d+")
    for y, line in enumerate(grid):
        for match in re.finditer(number_pattern, line):
            x0, x1 = match.span()
            n = int(match.group(0))
            boundaries = (
                [(x, y - 1) for x in range(x0 - 1, x1 + 1)]
                + [(x, y + 1) for x in range(x0 - 1, x1 + 1)]
                + [(x0 - 1, y), (x1, y)]
            )
            is_number_adjacntent = False
            for neighbour in boundaries:
                n_x, n_y = neighbour
                if n_x < 0 or n_x >= max_x or n_y < 0 or n_y >= max_y:
                    continue
                c = grid[n_y][n_x]
                if c == "*":
                    star_numbers[neighbour].append(n)
                if not c.isdigit() and c != ".":
                    is_number_adjacntent = True
            if is_number_adjacntent:
                numbers_connected.append(n)
    logger.info("Res a: %s", sum(numbers_connected))
    gears = [
        numbers[0] * numbers[1]
        for numbers in star_numbers.values()
        if len(numbers) == 2
    ]
    logger.info("Res b: %s", sum(gears))


def main():
    grid = read_input()
    count_numbers(grid)


if __name__ == "__main__":
    init_logging()
    main()
