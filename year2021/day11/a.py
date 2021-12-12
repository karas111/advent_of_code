import logging
import os
import copy
from typing import List, Set, Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Grid = List[List[int]]


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [
            [int(x) for x in line.strip()]
            for line in f if line.strip()
        ]


def neighbours(x, y, size):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            new_x, new_y = dx + x, dy + y
            if (
                new_x >= 0
                and new_x < size
                and new_y >= 0
                and new_y < size
                and (dx != 0 or dy != 0)
            ):
                yield (new_x, new_y)


def increase_energy(x: int, y: int, grid: Grid, already_flashed: Set[Tuple[int, int]]):
    size = len(grid)
    grid[y][x] += 1
    if grid[y][x] > 9 and (x, y) not in already_flashed:
        already_flashed.add((x, y))
        for xx, yy in neighbours(x, y, size):
            increase_energy(xx, yy, grid, already_flashed)


def simulate_step(grid: Grid) -> Tuple[Grid, int]:
    already_flashed = set()
    size = len(grid)
    for y in range(size):
        for x in range(size):
            increase_energy(x, y, grid, already_flashed)
    flashes = 0
    for y in range(size):
        for x in range(size):
            if grid[y][x] > 9:
                grid[y][x] = 0
                flashes += 1
    return flashes


def count_flashes(grid: Grid, steps=100):
    tot_flashes = 0
    while steps:
        tot_flashes += simulate_step(grid)
        steps -= 1
    return tot_flashes


def find_all_flashed(grid: Grid):
    steps = 0
    size = len(grid)
    while True:
        steps += 1
        if simulate_step(grid) == size ** 2:
            return steps


def main():
    grid = read_input()
    logger.info(f"Res a {count_flashes(copy.deepcopy(grid))}")
    logger.info(f"Res a {find_all_flashed(copy.deepcopy(grid))}")


if __name__ == "__main__":
    init_logging()
    main()
