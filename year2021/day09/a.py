import logging
import os
from typing import List

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
            if all(is_lower(terrain, x, y, dx, dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                res += val + 1
    return res


def main():
    terrain = read_input()
    logger.info(f"Res a {count_lows(terrain)}")


if __name__ == "__main__":
    init_logging()
    main()
