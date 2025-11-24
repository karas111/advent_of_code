import logging
import os
from collections import deque

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Cords = tuple[int, int, int]

D_VEC = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def read_cords() -> list[Cords]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def count_surface(cords: set[Cords]) -> int:
    res = 0
    for x, y, z in cords:
        for dx, dy, dz in D_VEC:
            res += (x + dx, y + dy, z + dz) not in cords
    return res


def count_exterior_surface(cords: set[Cords]) -> int:
    start = tuple(min(cord[i] for cord in cords) - 1 for i in range(3))
    end = tuple(max(cord[i] for cord in cords) + 1 for i in range(3))
    negative = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in negative:
            continue
        negative.add(node)
        for dv in D_VEC:
            neighbour = tuple(node[i] + dv[i] for i in range(3))
            if neighbour in cords:
                continue
            if any(start[i] > neighbour[i] or neighbour[i] > end[i] for i in range(3)):
                continue
            queue.append(neighbour)

    res = count_surface(negative)
    w, h, d = [end[i] - start[i] + 1 for i in range(3)]
    res -= 2 * (w * h + w * d + h * d)
    return res


def main():
    cords = set(read_cords())
    res = count_surface(cords)
    logger.info("Result a %d", res)
    res2 = count_exterior_surface(cords)
    logger.info("Result b %d", res2)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
