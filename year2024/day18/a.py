import logging
import os
from collections import deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

if INPUT_FILE.startswith("test"):
    MAX_SIZE = Cords(7, 7)
else:
    MAX_SIZE = Cords(71, 71)

MOVE_VEC = [
    Cords(-1, 0),
    Cords(1, 0),
    Cords(0, -1),
    Cords(0, 1),
]


def read_input() -> list[Cords]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            res.append(Cords(*map(int, line.strip().split(","))))
    return res


def reconcstruct_path(came_from, n):
    current = n
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    return list(reversed(path))


def get_shortest(fallen_bytes: list[Cords]) -> int:
    fallen_bytes_s = set(fallen_bytes)
    goal = MAX_SIZE - Cords(1, 1)
    queue = deque([(Cords(0, 0), 0, None)])
    visited = set()
    came_from = {}
    while queue:
        current, depth, parent = queue.popleft()
        if current in visited:
            continue
        came_from[current] = parent
        visited.add(current)
        if current == goal:
            p = reconcstruct_path(came_from, goal)
            return depth
        for dv in MOVE_VEC:
            neighbour = current + dv
            if (
                0 <= neighbour.x < MAX_SIZE.x
                and 0 <= neighbour.y < MAX_SIZE.y
                and neighbour not in fallen_bytes_s
            ):
                queue.append((neighbour, depth + 1, current))
    raise ValueError("Path not found")


def binary_search(fallen_bytes: list[Cords]) -> int:
    left, right = 0, len(fallen_bytes) - 1
    while left + 1 < right:
        i = (right + left) // 2
        found_path = True
        try:
            get_shortest(fallen_bytes[:i])
        except ValueError:
            found_path = False
        if found_path:
            left = i
        else:
            right = i
    return left


def main():
    fallen_bytes = read_input()
    with catchtime(logger):
        a = get_shortest(fallen_bytes[:1024])
        logger.info("Res A: %s", a)

        idx = binary_search(fallen_bytes)
        logger.info("Res B %s", fallen_bytes[idx])


if __name__ == "__main__":
    init_logging()
    main()
