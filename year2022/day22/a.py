import logging
import os
import re
from dataclasses import dataclass
from typing import NamedTuple

import numpy as np

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
            line = line.rstrip("\n")
            if not line:
                break
            grid.append(line)

        tokens = re.findall(r"\d+|[RL]", f.readline().strip())
        moves = [int(t) if t.isdigit() else t for t in tokens]

        return grid, moves


def solve_a(grid: list[str], moves: list):
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


@dataclass
class Cube:
    size: int
    faces: dict

    #   e----f
    #  /|   /|
    # a-+--b |
    # | g--+-h
    # |/   |/
    # c----d

    # We will store the original coordinates on each face of the Cube as 2d matrix.
    # Cube faces are named "abcd", "bfdh", "fehg", "eagc", "efab", "ghcd"

    FACES = ["abcd", "bfdh", "fehg", "eagc", "efab", "ghcd"]

    def rotate(self, dir: str):
        new_faces = {}
        if dir in "><":
            replaces = {"abcd": "bfdh", "bfdh": "fehg", "fehg": "eagc", "eagc": "abcd"}
            if dir == "<":
                new_faces = {a: self.faces[b] for a, b in replaces.items()}
            else:
                new_faces = {b: self.faces[a] for a, b in replaces.items()}

            # rotate counter clock wise
            k = 1 if dir == ">" else -1
            new_faces["efab"] = np.rot90(self.faces["efab"], k=k)
            new_faces["ghcd"] = np.rot90(self.faces["ghcd"], k=k)
        elif dir in "^v":
            if dir == "^":
                new_faces["abcd"] = np.flipud(self.faces["ghcd"])
                new_faces["ghcd"] = np.fliplr(self.faces["fehg"])
                new_faces["fehg"] = np.flipud(np.fliplr(self.faces["efab"]))
                new_faces["efab"] = self.faces["abcd"]
            else:
                new_faces["ghcd"] = np.flipud(self.faces["abcd"])
                new_faces["fehg"] = np.fliplr(self.faces["ghcd"])
                new_faces["efab"] = np.flipud(np.fliplr(self.faces["fehg"]))
                new_faces["abcd"] = self.faces["efab"]
            k = 1 if dir == "v" else -1
            new_faces["bfdh"] = np.rot90(self.faces["bfdh"], k=k)
            new_faces["eagc"] = np.rot90(self.faces["eagc"], k=-k)
        return Cube(self.size, new_faces)


MOVES_B = {">": Cords(1, 0), "v": Cords(0, 1), "<": Cords(-1, 0), "^": Cords(0, -1)}


def solve_b(grid: list[str], moves: list):
    size = 50 if INPUT_FILE == "input.txt" else 4
    start = Cords(grid[0].index("."), 0)
    cube = Cube(
        size,
        faces={
            face_name: np.full((size, size), None, dtype=object)
            for face_name in Cube.FACES
        },
    )
    seen = set()
    roll_cube = {"^": "^", "v": "v", "<": ">v<", ">": "<v>"}
    deroll_cube = {"^": "v", "v": "^", "<": ">^<", ">": "<^>"}

    def dfs(cords: Cords, cube: Cube):
        if cords in seen:
            return cube
        seen.add(cords)
        cube.faces["ghcd"] = np.array(
            [
                [Cords(cords.x + dx, cords.y + dy) for dx in range(size)]
                # [grid[cords.y + dy][cords.x + dx] for dx in range(size)]
                for dy in range(size)
            ]
        )
        for move, dc in MOVES_B.items():
            neighbour = cords + dc * size
            if (
                neighbour in seen
                or neighbour.y < 0
                or neighbour.y >= len(grid)
                or neighbour.x < 0
                or neighbour.x >= len(grid[neighbour.y])
                or grid[neighbour.y][neighbour.x] == " "
            ):
                continue

            rolls = roll_cube[move]
            derolls = deroll_cube[move]
            for rot in rolls:
                cube = cube.rotate(rot)
            cube = dfs(neighbour, cube)
            for rot in derolls:
                cube = cube.rotate(rot)
        return cube

    cube = dfs(start, cube)
    # we started with the first cube's face at the bottom. Rotate
    # it, so the starting point is in bottom left corner of front ("abcd") face
    cube = cube.rotate(">").rotate("^")
    cords = Cords(0, 0)
    direction = 1  # "v", change the direction because of the cube rotation
    dir_mod = (
        -1
    )  # we "wrap" the cube's net round, so we see a "reflection" of the original image on
    # the cubes face. Therefore, we the turns are reverted
    for move in moves:
        if move == "L":
            direction = (direction - 1 * dir_mod) % 4
        elif move == "R":
            direction = (direction + 1 * dir_mod) % 4
        else:
            dc = MOVES[direction]
            for _ in range(move):
                n_cube_cords = cords + dc
                n_cube = cube
                # if we cross an edge, we rotate the cube, so the "pointer" is always on front ("abcd") face
                if n_cube_cords.x < 0:
                    n_cube = cube.rotate(">")
                elif n_cube_cords.x >= size:
                    n_cube = cube.rotate("<")
                elif n_cube_cords.y < 0:
                    n_cube = cube.rotate("v")
                elif n_cube_cords.y >= size:
                    n_cube = cube.rotate("^")
                n_cube_cords = Cords(n_cube_cords.x % size, n_cube_cords.y % size)
                net_cords = n_cube.faces["abcd"][n_cube_cords.y][n_cube_cords.x]

                is_block = grid[net_cords.y][net_cords.x] == "#"
                if is_block:
                    break
                cords = n_cube_cords
                cube = n_cube
    net_cords = cube.faces["abcd"][cords.y][cords.x]
    prev_cords = cords - MOVES[direction]
    prev_net_cords = cube.faces["abcd"][prev_cords.y][prev_cords.x]
    d_net_vect = net_cords - prev_net_cords
    d_net_dir = MOVES.index(d_net_vect)
    logger.info("Last cords %s, dir %s", net_cords, d_net_dir)
    logger.info(
        "Res b: %d", (net_cords.y + 1) * 1000 + (net_cords.x + 1) * 4 + d_net_dir
    )


def main():
    grid, moves = read_input()
    state = solve_a(grid, moves)
    logger.info(
        "Result a %d",
        (state.cords.y + 1) * 1000 + (state.cords.x + 1) * 4 + state.direction,
    )
    solve_b(grid, moves)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
