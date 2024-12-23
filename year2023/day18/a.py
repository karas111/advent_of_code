import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable

from catch_time import catchtime
from cords.cords_2d import Cords
from graph import a_star
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


MOVE_VEC = {
    "R": Cords(1, 0),
    "D": Cords(0, 1),
    "L": Cords(-1, 0),
    "U": Cords(0, -1),
    "0": Cords(1, 0),
    "1": Cords(0, 1),
    "2": Cords(-1, 0),
    "3": Cords(0, -1),
}


def read_input() -> tuple[list[Cords], list[Cords]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        current0, current1 = Cords(0, 0), Cords(0, 0)
        res0, res1 = [current0], [current1]
        for l in f:
            direction, len_, color = l.strip().split()
            current0 = current0 + MOVE_VEC[direction] * int(len_)
            res0.append(current0)
            current1 = current1 + MOVE_VEC[color[-2]] * int(color[2:-2], base=16)
            res1.append(current1)

        return res0, res1


def calculate_area(cords: list[Cords]) -> int:
    # Shoelace formula
    res = 0
    for c0, c1 in zip(cords, cords[1:]):
        res += (c0.y + c1.y) * (c0.x - c1.x)
    assert res % 2 == 0
    return res // 2


def calculate_boundary_points(cords: list[Cords]) -> int:
    res = 0
    for c0, c1 in zip(cords, cords[1:]):
        res += abs(c1.y - c0.y) + abs(c1.x - c0.x)
    return res


def solve(cords: list[Cords]) -> int:
    area = calculate_area(cords)
    boundary_points = calculate_boundary_points(cords)
    assert boundary_points % 2 == 0
    # Pikc's theorem
    # A = i + b / 2 - 1
    # i = A - b / 2 + 1
    interior_points = area - boundary_points // 2 + 1
    return interior_points + boundary_points


def main():
    pointsa, pointsb = read_input()
    with catchtime(logger):
        logger.info("Res A: %s", solve(pointsa))
        logger.info("Res B: %s", solve(pointsb))


if __name__ == "__main__":
    init_logging()
    main()
