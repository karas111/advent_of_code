import logging
import os
from collections import deque
from typing import Iterable

from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Grid = list[str]


def find_char(to_find: str, grid: Grid) -> Iterable[Cords]:
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == to_find:
                yield Cords(x, y)


def read_grid() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


NEIGHBOURS = [Cords(-1, 0), Cords(1, 0), Cords(0, -1), Cords(0, 1)]


def get_elevation(c: str):
    if c == "S":
        return ord("a")
    if c == "E":
        return ord("z")
    return ord(c)


def bfs(start: Cords, end: Cords, grid: Grid) -> int:
    h, w = len(grid), len(grid[0])
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        node, path_l = queue.popleft()
        if node in visited:
            continue
        if node == end:
            return path_l
        node_val = get_elevation(grid[node.y][node.x])
        for d_cords in NEIGHBOURS:
            neighbour = node + d_cords
            if 0 <= neighbour.x < w and 0 <= neighbour.y < h:
                if get_elevation(grid[neighbour.y][neighbour.x]) - node_val <= 1:
                    queue.append((neighbour, path_l + 1))
        visited.add(node)


def main():
    grid = read_grid()
    start, end = next(find_char("S", grid)), next(find_char("E", grid))
    res = bfs(start, end, grid)
    logger.info("Result a %s", res)

    best_l = res
    for a_cords in find_char("a", grid):
        new_l = bfs(a_cords, end, grid)
        if new_l:
            best_l = min(new_l, best_l)
    logger.info("Result b %s", best_l)


if __name__ == "__main__":
    init_logging()
    main()
