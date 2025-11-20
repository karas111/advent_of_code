import logging
import os

from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Line = tuple[Cords, Cords]


def read_lines() -> list[Line]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            res_line = []
            for cord_2d in line.strip().split(" -> "):
                cords = Cords(*map(int, cord_2d.split(",")))
                res_line.append(cords)
            res.extend(list(zip(res_line, res_line[1:])))
    return res


def drop_sand(lines: list[Line], with_line: bool = False):
    seen = set()

    for start, end in lines:
        d_cord = end - start
        d_cord = d_cord // (abs(d_cord.x) + abs(d_cord.y))
        current = start
        while True:
            seen.add(current)
            if current == end:
                break
            current = current + d_cord
    max_h = max(c.y for c in seen) + 2
    if with_line:
        for x in range(500 - max_h, 500 + max_h + 1):
            seen.add(Cords(x, max_h))

    start_seen = len(seen)

    sand = Cords(500, 0)
    current = sand
    while True:
        if current.y >= max_h:
            logger.info("Detected leak at %s", current)
            break
        if current in seen:
            logger.info("Start covered in sand!")
            break
        below_pos = None
        for below_dx in [Cords(0, 1), Cords(-1, 1), Cords(1, 1)]:
            if (current + below_dx) not in seen:
                below_pos = current + below_dx
                break
        if below_pos is not None:
            current = below_pos
            continue
        seen.add(current)
        current = sand

    return len(seen) - start_seen


def main():
    lines = read_lines()
    seen = drop_sand(lines, False)
    logger.info("Result a %s", seen)
    seen = drop_sand(lines, True)
    logger.info("Result b %s", seen)


if __name__ == "__main__":
    init_logging()
    main()
