import logging
import math
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "test1.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def count_a(grid, move_x, move_y):
    counter = 0
    current_x, current_y = 0, 0
    while current_y < len(grid):
        if grid[current_y][current_x] == "#":
            # logger.info(f"Tree on x={current_x}, y={current_y}")
            counter += 1
        current_x = (current_x + move_x) % len(grid[0])
        current_y += move_y
    return counter


def main():
    grid = read_input()
    logger.info(f"Result a {count_a(grid, 3, 1)}")
    slopes_to_check = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees_count = [count_a(grid, x, y) for x, y in slopes_to_check]
    logger.info(f"Result b {trees_count}, res={math.prod(trees_count)}")


if __name__ == "__main__":
    init_logging()
    main()
