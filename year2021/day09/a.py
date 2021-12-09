import logging
import os
from typing import List, Set, Tuple
import math

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> List[List[int]]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            res.append([int(x) for x in line])
    return res


def is_lower(terrain, x, y, dx, dy):
    width, height = len(terrain[0]), len(terrain)
    if x + dx < 0 or x + dx >= width:
        return True
    if y + dy < 0 or y + dy >= height:
        return True
    return terrain[y][x] < terrain[y + dy][x + dx]


def count_lows(terrain: List[List[int]]) -> int:
    res = 0
    for y, row in enumerate(terrain):
        for x, val in enumerate(row):
            if all(
                is_lower(terrain, x, y, dx, dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            ):
                res += val + 1
    return res


def bfs(terrain: List[List[int]], x: int, y: int) -> Set[Tuple[int, int]]:
    width, height = len(terrain[0]), len(terrain)
    visited = set()
    queue = [(x, y)]
    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if terrain[y][x] == 9:
            continue
        visited.add((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            queue.append((x + dx, y + dy))
    return visited


def find_basins(terrain: List[List[int]]) -> List[int]:
    visited = set()
    res = []
    for y, row in enumerate(terrain):
        for x, val in enumerate(row):
            if val == 9 or (x, y) in visited:
                continue
            basin_visited = bfs(terrain, x, y)
            visited.update(basin_visited)
            res.append(len(basin_visited))
    return res


def main():
    terrain = read_input()
    logger.info(f"Res a {count_lows(terrain)}")
    basins = sorted(find_basins(terrain))
    logger.info(f"Res b {math.prod(basins[-3:])}")


if __name__ == "__main__":
    init_logging()
    main()
