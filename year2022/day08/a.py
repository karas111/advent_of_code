import logging
import os

from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Grid = list[list[int]]


def read_grid() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [list(map(int, line.strip())) for line in f]


def find_visibile(grid: Grid) -> list[list[bool]]:
    res = [[True] * len(row) for row in grid]
    for y, row in enumerate(grid):
        max_h = -1
        for x, n in enumerate(row):
            if max_h >= n:
                res[y][x] = False
            max_h = max(n, max_h)
    return res


def find_visibile_from_all_directions(grid: Grid) -> list[list[bool]]:
    res = find_visibile(grid)
    for _ in range(3):
        grid = [list(row) for row in zip(*grid[::-1])]
        sub_res = find_visibile(grid)
        res = [list(row) for row in zip(*res[::-1])]
        res = [
            [res[y][x] or sub_res[y][x] for x in range(len(res[y]))]
            for y in range(len(res))
        ]
    return [list(row) for row in zip(*res[::-1])]


def count_viewing_score(grid: Grid, start_cords: Cords) -> int:
    start_height = grid[start_cords.y][start_cords.x]
    max_x, max_y = len(grid[0]), len(grid)
    res = 1
    for d_cords in [Cords(-1, 0), Cords(1, 0), Cords(0, -1), Cords(0, 1)]:
        cords = start_cords
        while True:
            cords += d_cords
            is_beyond_edge = (
                0 > cords.x or cords.x >= max_x or 0 > cords.y or cords.y >= max_y
            )

            if is_beyond_edge or grid[cords.y][cords.x] >= start_height:
                direction_len = (
                    abs(start_cords.x - cords.x)
                    + abs(start_cords.y - cords.y)
                    - is_beyond_edge
                )
                res *= direction_len
                break
    return res


def find_best_viewing_point(grid: Grid) -> int:
    current_score = -1
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            current_score = max(count_viewing_score(grid, Cords(x, y)), current_score)
    return current_score


def main():
    grid = read_grid()
    res = find_visibile_from_all_directions(grid)
    logger.info("Result a %s", sum(sum(row) for row in res))
    res = find_best_viewing_point(grid)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    main()
