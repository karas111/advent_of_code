import logging
from typing import Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

Point = Tuple[int, int]


def is_in_target(current: Point, start: Point, end: Point) -> bool:
    return start[0] <= current[0] <= end[0] and start[1] >= current[1] >= end[1]


def is_too_far(current: Point, end: Point) -> bool:
    return current[0] > end[0] or current[1] < end[1]


def simulate_one(vx: int, vy: int, start: Point, end: Point) -> int:
    current = (0, 0)
    max_h = 0
    hits = set()
    while not is_too_far(current, end):
        if is_in_target(current, start, end):
            hits.add(current)
        max_h = max(max_h, current[1])
        current = current[0] + vx, current[1] + vy
        vx = max(0, vx - 1)
        vy -= 1
    if hits:
        return max_h
    return None


def simulate(start: Point, end: Point) -> Tuple[int, int]:
    count_hits = 0
    max_h = 0
    for vx in range(end[0] + 1):
        for vy in range(end[1], -end[1] + 1):
            height = simulate_one(vx, vy, start, end)
            if height is not None:
                count_hits += 1
                max_h = max(max_h, height)
    return max_h, count_hits


def main():
    # start, end = (20, -5), (30, -10)
    start, end = (236, -58), (262, -78)
    logger.info(f"Res a {simulate(start, end)}")


if __name__ == "__main__":
    init_logging()
    main()
