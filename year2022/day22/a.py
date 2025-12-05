import bisect
import logging
import operator
import os
import re
from collections import namedtuple
from typing import NamedTuple

from sympy import Eq, symbols
from sympy.solvers import solve

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVES = [Cords(1, 0), Cords(0, 1), Cords(-1, 0), Cords(0, -1)]


class State(NamedTuple):
    cords: Cords
    direction: int


def read_input() -> tuple[list[str], str]:
    grid = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.rstrip()
            if not line:
                break
            grid.append(line)

        tokens = re.findall(r"\d+|[RL]", f.readline().strip())
        moves = [int(t) if t.isdigit() else t for t in tokens]

        return grid, moves


def solve(grid: list[str], moves: list):
    state = State(Cords(grid[0].index("."), 0), 0)

    max_l = max(len(line) for line in grid)
    grid = [f" {line}" + " " * (max_l - len(line) + 1) for line in grid]
    grid = [" " * len(grid[0])] + grid + [" " * len(grid[0])]

    def create_map(g: list[str]):
        rows = []
        for line in g[1:-1]:
            row = []
            for idx in range(1, len(line) - 1):
                # add left wall
                if line[idx] != " " and line[idx - 1] == " ":
                    row.append(idx - 1)
                # add rock
                if line[idx] == "#":
                    row.append(idx)
                # add right wall
                if line[idx] != " " and line[idx + 1] == " ":
                    row.append(idx + 1)
            # all idx are moved 1 because of the empty space
            row = [idx - 1 for idx in row]
            rows.append(row)
        return rows

    rows = create_map(grid)
    columns = create_map(list(zip(*grid[::])))

    for move in moves:
        if move == "L":
            state = State(state.cords, (state.direction - 1) % 4)
        elif move == "R":
            state = State(state.cords, (state.direction + 1) % 4)
        else:
            is_row = state.direction in (0, 2)
            d_c = MOVES[state.direction].x if is_row else MOVES[state.direction].y
            current_c = state.cords.x if is_row else state.cords.y
            line = rows[state.cords.y] if is_row else columns[state.cords.x]
            for _ in range(move):
                n_c = current_c + d_c
                if n_c == line[0]:
                    n_c = line[-1] - 1
                elif n_c == line[-1]:
                    n_c = line[0] + 1

                if n_c in line:  # binary search to speed up
                    break
                else:
                    current_c = n_c
            n_tot_cords = (
                Cords(current_c, state.cords.y)
                if is_row
                else Cords(state.cords.x, current_c)
            )
            state = State(n_tot_cords, state.direction)
    return state


def main():
    grid, moves = read_input()
    state = solve(grid, moves)
    logger.info(
        "Result a %d",
        (state.cords.y + 1) * 1000 + (state.cords.x + 1) * 4 + state.direction,
    )


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
