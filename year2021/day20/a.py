import logging
import os
from typing import Iterable, Tuple, List, Set

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Point = Tuple[int, int]


def read_input() -> Tuple[int, Set[Point]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        algo_str = list(reversed(f.readline().strip()))
        algo = bits_to_number(bit == "#" for bit in algo_str)

        points = set()
        for y, line in enumerate(f.readlines()[1:]):
            if not line:
                continue
            for x, c in enumerate(line):
                if c == "#":
                    points.add((x, y))
    return algo, points


def bits_to_number(bits: Iterable[bool]) -> int:
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out


def get_number(decode_algo: int, bits: Iterable[bool]):
    idx = bits_to_number(bits)
    return (decode_algo >> idx) & 1


def neighbours(x, y):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            yield (dx + x, dy + y)


def get_ranges(points: Set[Point]) -> Tuple[Point, Point]:
    p = next(iter(points))
    min_x = min_y = p[0]
    max_x = max_y = p[1]
    for point in points:
        min_x = min(min_x, point[0])
        max_x = max(max_x, point[0])
        min_y = min(min_y, point[1])
        max_y = max(max_y, point[1])
    return (min_x, min_y), (max_x, max_y)


def get_bit(
    point: Point, points: List[Point], n: int, min_point: Point, max_point: Point
) -> bool:
    is_in = all(min_point[idx] <= point[idx] <= max_point[idx] for idx in range(2))
    if is_in:
        return point in points
    else:
        return n % 2 == 1


def apply_algo(algo: int, points: Set[Point], n: int = 2) -> Set[Point]:
    for step in range(n):
        new_points = set()
        min_point, max_point = get_ranges(points)
        for x in range(min_point[0] - 1, max_point[0] + 2):
            for y in range(min_point[1] - 1, max_point[1] + 2):
                bits = [
                    get_bit(neighbour, points, step, min_point, max_point)
                    for neighbour in neighbours(x, y)
                ]
                new_val = get_number(algo, bits)
                if new_val:
                    new_points.add((x, y))
        points = new_points
    return points


def main():
    algo, points = read_input()
    new_points = apply_algo(algo, points, n=2)
    logger.info(f"Res a {len(new_points)}")
    new_points = apply_algo(algo, points, n=50)
    logger.info(f"Res b {len(new_points)}")


if __name__ == "__main__":
    init_logging()
    main()
