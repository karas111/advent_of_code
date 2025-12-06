import logging
import os
from collections import Counter
from typing import Optional

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

TO_CHECK = [
    [Cords(x, -1) for x in range(-1, 2)],  # north
    [Cords(x, 1) for x in range(-1, 2)],  # south
    [Cords(-1, y) for y in range(-1, 2)],  # west
    [Cords(1, y) for y in range(-1, 2)],  # east
]


def read_input() -> set[Cords]:
    grid = set()
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    grid.add(Cords(x, y))
        return grid


def simulate(grid: set[Cords], rounds: Optional[int] = 10) -> set[Cords]:
    direction_pref = 0
    i = 0
    while rounds is None or i < rounds:
        where_to_move = {}
        # phase one
        for elf in grid:
            # by default not move at all
            where_to_move[elf] = elf
            # not move at all
            all_neighbours = [
                Cords(x, y) + elf for x in range(-1, 2) for y in range(-1, 2)
            ]
            if all(n_c == elf or n_c not in grid for n_c in all_neighbours):
                continue
            # check the directions
            for direction_mod in range(4):
                direction = (direction_pref + direction_mod) % 4
                if all((elf + c) not in grid for c in TO_CHECK[direction]):
                    where_to_move[elf] = elf + TO_CHECK[direction][1]
                    break

        # phase two
        new_grid = set()
        to_move_counter = Counter(where_to_move.values())
        for elf in grid:
            # not move
            if elf == where_to_move[elf]:
                new_grid.add(elf)
                continue
            new_loc = where_to_move[elf]
            if to_move_counter[new_loc] == 1:
                new_grid.add(new_loc)
            else:
                new_grid.add(elf)
        if grid == new_grid:
            return grid, i + 1
        grid = new_grid
        direction_pref = (direction_pref + 1) % 4
        i += 1
    return grid, i


def print_grid(grid: set[Cords]) -> str:
    lines = []
    for y in range(min(c.y for c in grid), max(c.y for c in grid) + 1):
        line = "".join(
            "#" if Cords(x, y) in grid else "."
            for x in range(min(c.x for c in grid), max(c.x for c in grid) + 1)
        )
        lines.append(line)
    return "\n".join(lines)


def count_free_spaces(grid: set[Cords]) -> int:
    w = max(c.x for c in grid) - min(c.x for c in grid) + 1
    h = max(c.y for c in grid) - min(c.y for c in grid) + 1
    return w * h - len(grid)


def main():
    grid = read_input()
    grid2, _ = simulate(grid, rounds=10)
    res = count_free_spaces(grid2)
    logger.info("Result a %s", res)
    grid2, rounds = simulate(grid, rounds=None)
    logger.info("Result b %s", rounds)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
