import logging
import os
from collections import defaultdict
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Cords = tuple[int, int]


def read_input() -> tuple[dict[str, list[Cords]], Cords]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = defaultdict(list)
        x, y = 0, 0
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, c in enumerate(line):
                if c != ".":
                    res[c].append((x, y))
        return res, (x + 1, y + 1)


def find_antinodes(
    antennas: dict[str, list[Cords]], boundaries: Cords, multipliers: Iterable[int]
) -> set[Cords]:
    res = set()
    max_x, max_y = boundaries
    for coords in antennas.values():
        for idx, (x0, y0) in enumerate(coords):
            for x1, y1 in coords[idx + 1 :]:
                for multiplier in multipliers:
                    dx, dy = (x1 - x0) * multiplier, (y1 - y0) * multiplier
                    x, y = x0 + dx, y0 + dy
                    if 0 <= x < max_x and 0 <= y < max_y:
                        res.add((x, y))
    return res


def main():
    antennas, boundaries = read_input()
    antionodes = find_antinodes(antennas, boundaries, multipliers=[-1, 2])
    logger.info("Res a %s", len(antionodes))
    antionodes = find_antinodes(
        antennas, boundaries, multipliers=range(-max(boundaries), max(boundaries) + 1)
    )
    logger.info("Res b %s", len(antionodes))


if __name__ == "__main__":
    init_logging()
    main()
