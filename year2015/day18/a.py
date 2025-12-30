import logging
import os

import catch_time
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


MOVES = [Cords(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0]


def simulate(grid: list[str], steps: int, part_b: bool = False):
    CORNERS = {
        Cords(
            0,
            0,
        ),
        Cords(0, len(grid) - 1),
        Cords(len(grid[0]) - 1, 0),
        Cords(len(grid[0]) - 1, len(grid) - 1),
    }

    def count_neighbours_on(cords: Cords, grid: list[str]) -> int:
        res = 0
        for dc in MOVES:
            n_c = cords + dc
            res += (
                n_c.x >= 0
                and n_c.x < len(grid[0])
                and n_c.y >= 0
                and n_c.y < len(grid)
                and grid[n_c.y][n_c.x] == "#"
            )
        return res

    for _ in range(steps):
        new_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                cords = Cords(x, y)
                neighbours_on = count_neighbours_on(cords, grid)
                if part_b and cords in CORNERS:
                    new_grid[y][x] = "#"
                elif c == "#":
                    new_grid[y][x] = "#" if neighbours_on in (2, 3) else "."
                else:
                    new_grid[y][x] = "#" if neighbours_on == 3 else "."
        grid = new_grid
    return sum(line.count("#") for line in grid)


def main():
    grid = read_input()
    res = simulate(grid, 100)
    logger.info("Res a: %s", res)
    res = simulate(grid, 100, part_b=True)
    logger.info("Res b: %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
