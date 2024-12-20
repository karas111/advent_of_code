import logging
import os
from collections import defaultdict, deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVE_VEC = [
    Cords(1, 0),
    Cords(0, 1),
    Cords(-1, 0),
    Cords(0, -1),
]

Grid = list[str]


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def bfs(g: Grid, start: tuple[Cords, int]) -> int:
    queue = deque([start])
    energized = defaultdict(int)
    while queue:
        current, move_idx = queue.popleft()
        if (
            current.x < 0
            or current.x >= len(g[0])
            or current.y < 0
            or current.y >= len(g)
        ):
            continue
        if energized[(current, move_idx)] > 1:
            continue
        energized[(current, move_idx)] += 1

        move_vertical = move_idx % 2
        c = g[current.y][current.x]
        if c == "." or (move_vertical and c == "|") or (not move_vertical and c == "-"):
            queue.append((current + MOVE_VEC[move_idx], move_idx))
        elif (move_vertical and c == "-") or (not move_vertical and c == "|"):
            new_move_idx = (move_idx + 1) % 4
            queue.append((current + MOVE_VEC[new_move_idx], new_move_idx))
            new_move_idx = (move_idx - 1) % 4
            queue.append((current + MOVE_VEC[new_move_idx], new_move_idx))
        elif c == "/":
            move_mod = 1 if move_vertical else -1
            new_move_idx = (move_idx + move_mod) % 4
            queue.append((current + MOVE_VEC[new_move_idx], new_move_idx))
        elif c == "\\":
            move_mod = -1 if move_vertical else 1
            new_move_idx = (move_idx + move_mod) % 4
            queue.append((current + MOVE_VEC[new_move_idx], new_move_idx))
        else:
            raise ValueError("unexpected char")
    total_energized = defaultdict(int)
    for (cords, _), v in energized.items():
        total_energized[cords] += v
    return len([v for v in total_energized.values() if v >= 1])


def solve_part2(g: Grid):
    x_size, y_size = len(g[0]), len(g)
    starts = (
        [(Cords(0, y), 0) for y in range(y_size)]
        + [(Cords(x, 0), 1) for x in range(x_size)]
        + [(Cords(x_size - 1, y), 2) for y in range(y_size)]
        + [(Cords(x, (y_size - 1)), 3) for x in range(x_size)]
    )
    return max(bfs(g, start) for start in starts)


def main():
    g = read_input()
    with catchtime(logger):
        logger.info("Res A: %s", bfs(g, (Cords(0, 0), 0)))
        logger.info("Res B: %s", solve_part2(g))


if __name__ == "__main__":
    init_logging()
    main()
