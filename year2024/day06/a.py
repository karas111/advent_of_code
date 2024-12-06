import logging
import os
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Map = list[str]
Cords = tuple[int, int]


def read_input() -> Map:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line.strip()]


def get_starting_pos(m: Map) -> Cords:
    for y, line in enumerate(m):
        for x, c in enumerate(line):
            if c == "^":
                return (x, y)
    raise ValueError("not found starting position")


MOVEMENT_VEC = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]


def walk_map(m: Map, pos: Cords, movement: int = 0) -> set[Cords]:
    visited = set()
    visited_with_dir = set()
    while True:
        dx, dy = MOVEMENT_VEC[movement]
        if (pos, movement) in visited_with_dir:
            return visited, True
        visited_with_dir.add((pos, movement))
        visited.add(pos)

        x, y = pos[0] + dx, pos[1] + dy
        if x < 0 or x >= len(m[0]) or y < 0 or y >= len(m):
            return visited, False
        if m[y][x] == "#":
            movement = (movement + 1) % 4
        else:
            pos = (x, y)


def map_generator(m: Map, visited: set[Cords]) -> Iterable[Map]:
    m = [list(line) for line in m]
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == "." and (x, y) in visited:
                m[y][x] = "#"
                yield m
                m[y][x] = "."


def main():
    m = read_input()
    starting_pos = get_starting_pos(m)
    visitied, cycle = walk_map(m, starting_pos)
    logger.info("Res a %s, %s", len(visitied), cycle)
    cycles = [walk_map(new_m, starting_pos)[1] for new_m in map_generator(m, visitied)]
    logger.info("Res b %s", sum(cycles))


if __name__ == "__main__":
    init_logging()
    main()
