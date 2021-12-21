from typing import Counter, List, Iterable, Tuple, Optional
from functools import cached_property
import operator
from itertools import product, permutations
import os
import logging
from year2019.utils import init_logging


logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Point:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z

    def __repr__(self) -> str:
        return str(self.to_tuple)

    def _point_op(self, other: "Point", op) -> "Point":
        return Point(op(self.x, other.x), op(self.y, other.y), op(self.z, other.z))

    def __add__(self, other: "Point") -> "Point":
        return self._point_op(other, operator.add)

    def __sub__(self, other: "Point") -> "Point":
        return self._point_op(other, operator.sub)

    def __mul__(self, other: "Point") -> "Point":
        return self._point_op(other, operator.mul)

    def __hash__(self) -> int:
        return hash(self.to_tuple)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Point) and self.to_tuple == __o.to_tuple

    @cached_property
    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)


class Scanner:
    def __init__(
        self, id: int, detected_points: List[Point], location: Optional[Point] = None
    ) -> None:
        self.id = id
        self.detected_points = detected_points
        self.location: Point = location


def generate_rotations(points: List[Point]) -> Iterable[List[Point]]:
    for perm in permutations(range(3)):
        for signs in product([-1, 1], repeat=3):
            signs = Point(*signs)
            rotation = []
            for point in points:
                new_point = Point(*[point.to_tuple[i] for i in perm]) * signs
                rotation.append(new_point)
            yield rotation


def check_scanner(
    located_scanner: Scanner, other: Scanner
) -> Tuple[List[Point], Point]:
    for rotation in generate_rotations(other.detected_points):
        distances = Counter()
        for other_point in rotation:
            for located_point in located_scanner.detected_points:
                distances[other_point - located_point] += 1

        for delta, count in distances.items():
            if count >= 12:
                return rotation, delta
    return None, None


def locate_scanners(scanners: List[Scanner]) -> List[Scanner]:
    located_scanners = {0: Scanner(0, scanners[0].detected_points, Point(0, 0, 0))}
    checked_pairs = set()
    while len(located_scanners) != len(scanners):
        for not_located_scanner in scanners:
            if not_located_scanner.id in located_scanners:
                continue
            for located_scanner in located_scanners.values():
                if (located_scanner.id, not_located_scanner.id) in checked_pairs:
                    continue
                checked_pairs.add((located_scanner.id, not_located_scanner.id))
                rotation_points, delta = check_scanner(
                    located_scanner, not_located_scanner
                )
                if delta:
                    location = Point(0, 0, 0) - delta
                    detected_points = [point + location for point in rotation_points]
                    located_scanners[not_located_scanner.id] = Scanner(
                        not_located_scanner.id, detected_points, location
                    )
                    logger.info(f"Found scanner {not_located_scanner.id}")
                    break
    return list(located_scanners.values())


def read_input() -> List[Scanner]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        scanners_str = f.read().strip().split("\n\n")
        scanners = []
        for idx, scanner_str in enumerate(scanners_str):
            points = scanner_str.split("\n")[1:]
            points = [
                Point(*[int(x) for x in point_str.split(",")]) for point_str in points
            ]
            scanners.append(Scanner(idx, points))
    return scanners


def get_all_points(scanners: List[Scanner]) -> List[Point]:
    return {p for scanner in scanners for p in scanner.detected_points}


def get_max_size(scanners: List[Scanner]) -> int:
    return max(
        sum([abs(x) for x in (other.location - scanner.location).to_tuple])
        for scanner in scanners
        for other in scanners
    )


def main():
    scanners = read_input()
    located_scanners = locate_scanners(scanners)
    logger.info(f"Res a {len(get_all_points(located_scanners))}")
    logger.info(f"Res b {get_max_size(located_scanners)}")


if __name__ == "__main__":
    init_logging()
    main()
