import logging
import os
from dataclasses import dataclass

from pyparsing import deque
from sortedcontainers import SortedList

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


@dataclass
class Cords:
    x: int
    y: int
    z: int


class Cube:
    def __init__(self, start: Cords, end: Cords):
        self.start = start
        self.end = end
        self.supports = []
        self.supported_by = []

    @property
    def max_z(self) -> int:
        return max(self.start.z, self.end.z)

    @property
    def min_z(self) -> int:
        return min(self.start.z, self.end.z)

    def add_supports(self, cube: "Cube") -> None:
        self.supports.append(cube)

    def add_supported_by(self, cube: "Cube") -> None:
        self.supported_by.append(cube)

    def does_support(self, cube: "Cube") -> bool:
        if self.max_z >= cube.min_z:
            return False
        x0_s, x0_e = sorted([self.start.x, self.end.x])
        y0_s, y0_e = sorted([self.start.y, self.end.y])
        x1_s, x1_e = sorted([cube.start.x, cube.end.x])
        y1_s, y1_e = sorted([cube.start.y, cube.end.y])
        if x0_s > x1_e or x0_e < x1_s or y0_s > y1_e or y0_e < y1_s:
            return False
        return True

    def fall(self, dz: int) -> None:
        self.start.z -= dz
        self.end.z -= dz

    def __repr__(self):
        return f"<{self.start}, {self.end}>"


def read_input() -> list[Cube]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = []
        for line in f:
            start_str, end_str = line.strip().split("~")
            start = Cords(*map(int, start_str.split(",")))
            end = Cords(*map(int, end_str.split(",")))
            res.append(Cube(start, end))
    return res


def solve(cubes: list[Cube]) -> int:
    cubes = list(sorted(cubes, key=lambda c: c.max_z))
    below: SortedList[Cube] = SortedList(key=lambda c: -c.max_z)
    for cube in cubes:
        z_below = None
        for below_cube in below:
            if z_below is not None and z_below > below_cube.max_z:
                break
            if below_cube.does_support(cube):
                z_below = below_cube.max_z
                below_cube.add_supports(cube)
                cube.add_supported_by(below_cube)
        if z_below is None:
            z_below = 0
        dz = cube.min_z - z_below - 1
        cube.fall(dz)
        below.add(cube)

    res = 0
    for cube in cubes:
        if all(len(other_c.supported_by) > 1 for other_c in cube.supports):
            res += 1
    return res


def solve2(cubes: list[Cube]) -> int:
    def bfs(start: Cube):
        queue = deque([start])
        fallen = set()
        while queue:
            current = queue.popleft()
            if current in fallen:
                continue
            if current != start and any(n not in fallen for n in current.supported_by):
                continue
            fallen.add(current)
            for n in current.supports:
                queue.append(n)
        return len(fallen) - 1

    return sum(bfs(c) for c in cubes)


def main():
    cubes = read_input()
    with catchtime(logger):
        res = solve(cubes)
        logger.info("Res A: %d", res)

    with catchtime(logger):
        res = solve2(cubes)
        logger.info("Res B: %d", res)


if __name__ == "__main__":
    init_logging()
    main()
