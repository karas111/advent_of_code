import logging
import os
from typing import Dict, Tuple, List
from heapdict import heapdict

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> Tuple[str, Dict[str, str]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [[int(x) for x in line.strip()] for line in f if line]


def neighbours(x, y, grid):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = dx + x, dy + y
        if new_x >= 0 and new_x < len(grid[0]) and new_y >= 0 and new_y < len(grid):
            yield (new_x, new_y)


def search_path_weight(grid: List[List[int]]) -> int:
    queue = heapdict()
    queue[(0, 0)] = 0
    visited = set()
    while queue:
        cords, weight = queue.popitem()
        x, y = cords
        if cords in visited:
            continue
        visited.add(cords)
        if cords == (len(grid[0]) - 1, len(grid) - 1):
            logger.info("Found exit %s = %d", cords, weight)
            return weight
        for nx, ny in neighbours(x, y, grid):
            new_weight = weight + grid[ny][nx]
            curr_weight = queue.get((nx, ny), -1)
            if curr_weight < 0 or curr_weight > new_weight:
                queue[(nx, ny)] = new_weight
    raise ValueError("Exit not found")


def terraform_grid(grid: List[List[int]]) -> List[List[int]]:
    width, height = len(grid[0]), len(grid)
    new_grid = [[0] * len(grid[0] * 5) for _ in range(len(grid) * 5)]
    for xx in range(5):
        for yy in range(5):
            for y, line in enumerate(grid):
                for x, val in enumerate(line):
                    new_val = val + xx + yy
                    if new_val > 9:
                        new_val -= 9
                    new_grid[y + height * yy][x + width * xx] = new_val
    return new_grid


def main():
    grid = read_input()
    logger.info(f"Res a {search_path_weight(grid)}")
    grid = terraform_grid(grid)
    logger.info(f"Res b {search_path_weight(grid)}")


if __name__ == "__main__":
    init_logging()
    main()
