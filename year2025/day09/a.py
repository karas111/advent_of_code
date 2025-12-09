import logging
import os

from shapely.geometry import Polygon, box

import catch_time
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[Cords]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for l in f:
            x, y = l.strip().split(",")
            res.append(Cords(int(x), int(y)))
    return res


def solve(grid: list[Cords], part_b: bool) -> int:
    p = Polygon((c.x, c.y) for c in grid)

    def is_valid(c1: Cords, c2: Cords) -> bool:
        if not part_b:
            return True
        rec = box(min(c1.x, c2.x), min(c1.y, c2.y), max(c1.x, c2.x), max(c1.y, c2.y))
        return p.contains(rec)

    max_ = -1
    for idx, c1 in enumerate(grid[:-1]):
        for c2 in grid[idx + 1 :]:
            dc = c1 - c2
            if not is_valid(c1, c2):
                continue
            max_ = max(max_, (abs(dc.x) + 1) * (abs(dc.y) + 1))
    return max_


def main():
    grid = read_input()
    res = solve(grid, False)
    logger.info("Result a %s", res)
    res = solve(grid, True)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
