import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


M_VEC = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

Grid = list[list[str]]
Cords = tuple[int, int]


def read_input() -> tuple[Grid, str]:
    g = []
    moves = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            if not line.strip():
                break
            g.append(list(line.strip()))
        for line in f:
            moves.append(line.strip())
    return g, "".join(moves)


def get_current_cord(g: Grid) -> Cords:
    for y, line in enumerate(g):
        for x, c in enumerate(line):
            if c == "@":
                return x, y
    raise ValueError("Not found starting pos")


def count_score(g: Grid) -> int:
    res = 0
    for y, line in enumerate(g):
        for x, c in enumerate(line):
            if c in "O[":
                res += 100 * y + x
    return res


def modify_map(g: Grid) -> Grid:
    res = []
    for line in g:
        n_line = []
        res.append(n_line)
        for c in line:
            if c in ".#":
                n_line.extend(c * 2)
            elif c == "O":
                n_line.extend("[]")
            elif c == "@":
                n_line.extend("@.")
    return res


def move(g: Grid, moves: str) -> Grid:
    x, y = get_current_cord(g)
    for m in moves:
        dx, dy = M_VEC[m]
        to_move = []
        n_x, n_y = x, y
        front_points = {(n_x, n_y)}
        move_allowed = True
        while True:
            new_front_points = set()
            for n_x, n_y in front_points:
                n_x, n_y = n_x + dx, n_y + dy
                n_c = g[n_y][n_x]
                if (n_c in "[]" and dy == 0) or n_c == "O":
                    new_front_points.add((n_x, n_y))
                elif n_c == "[" and y != 0:
                    new_front_points.add((n_x, n_y))
                    new_front_points.add((n_x + 1, n_y))
                elif n_c == "]" and y != 0:
                    new_front_points.add((n_x, n_y))
                    new_front_points.add((n_x - 1, n_y))
                elif n_c == ".":
                    continue
                elif n_c == "#":
                    move_allowed = False
                    break
            if not move_allowed:
                break
            to_move.extend(front_points)
            front_points = new_front_points
            if not front_points:
                break
        if not move_allowed:
            continue

        for n_x, n_y in reversed(to_move):
            c = g[n_y][n_x]
            g[n_y][n_x] = "."
            g[n_y + dy][n_x + dx] = c
        x, y = x + dx, y + dy
        # logger.info("\n%s", "\n".join("".join(line) for line in g))


def main():
    g, moves = read_input()
    with catchtime(logger):
        move(g, moves)
        logger.info("Res A %s", count_score(g))

    g, moves = read_input()
    g = modify_map(g)
    with catchtime(logger):
        move(g, moves)
        logger.info("Res B %s", count_score(g))


if __name__ == "__main__":
    init_logging()
    main()
