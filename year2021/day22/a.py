import logging
import os
from typing import Counter, NamedTuple, Tuple, List, Optional
import math
import re
import copy

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Point = Tuple[int, int, int]


class Cube(NamedTuple):
    p1: Point
    p2: Point


class Step(NamedTuple):
    cube: Cube
    on: bool


def intersection(c1: Cube, c2: Cube) -> Optional[Cube]:
    p1 = tuple(max(c1.p1[i], c2.p1[i]) for i in range(3))
    p2 = tuple(min(c1.p2[i], c2.p2[i]) for i in range(3))
    if all(p2[i] >= p1[i] for i in range(3)):
        return Cube(p1, p2)


def volume(cube: Cube):
    return math.prod(cube.p2[i] - cube.p1[i] + 1 for i in range(3))


def read_input() -> List[Step]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = []
        for line in f:
            if not line:
                continue
            cords = list(map(int, re.findall("-?\d+", line)))
            cube = Cube(
                p1=tuple(cords[x] for x in range(0, 6, 2)),
                p2=tuple(cords[x] for x in range(1, 6, 2)),
            )
            res.append(Step(cube, line.startswith("on")))
        return res


def count_volume(steps: List[Step]) -> int:
    cubes = Counter()
    for step in steps:
        for other_cube in copy.copy(cubes):
            inter = intersection(step.cube, other_cube)
            if inter:
                cubes[inter] -= cubes[other_cube]
        if step.on:
            cubes[step.cube] += 1

    return sum(volume(cube) * mult for cube, mult in cubes.items())


def part1(steps: List[Step]) -> int:
    steps = [
        step
        for step in steps
        if all(-50 <= x <= 50 for point in step.cube for x in point)
    ]
    return count_volume(steps)


def main():
    steps = read_input()
    logger.info(f"Res A {part1(steps)}")
    logger.info(f"Res B {count_volume(steps)}")


if __name__ == "__main__":
    init_logging()
    main()
