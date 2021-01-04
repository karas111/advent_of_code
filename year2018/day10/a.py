import logging
import time
import os
import re
from typing import List
from collections import namedtuple
import numpy as np

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Point = namedtuple("Point", ["pos", "velocity"])


def parse_input() -> List[Point]:
    def parse_point(line) -> Point:
        coords = re.match("position=<(.*), (.*)> velocity=<(.*), (.*)>", line).groups()
        coords = [int(x.strip()) for x in coords]
        return Point(np.array(coords[0:2]), np.array(coords[2:4]))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_point(line.strip()) for line in f.readlines() if line]


def print_points(points, verbose=True):
    points = [point.pos for point in points]
    pos_x = [pos[0] for pos in points]
    pos_y = [pos[1] for pos in points]
    delta = np.array([min(pos_x), min(pos_y)])
    ranges = np.array([max(pos_x)+1, max(pos_y)+1]) - delta
    if sum(ranges) < 73:
        print("\nMAPS\n")
        points = [point - delta for point in points]
        res = [["."] * ranges[0] for _ in range(ranges[1])]
        for point in points:
            res[point[1]][point[0]] = "#"
        res = ["".join(line) for line in res]
        print("\n".join(res))
    return ranges


def simulate_step(points):
    return [
        Point(point.pos + point.velocity, point.velocity)
        for point in points
    ]


def simulate(points, start, end):
    for _ in range(start):
        points = simulate_step(points)
    ranges = []
    ranges.append(print_points(points, verbose=False))
    for i in range(start, end):
        # print(f"{i} seconds")
        points = simulate_step(points)
        ranges.append(print_points(points, verbose=False))
    return ranges


def main():
    points = parse_input()
    ranges = simulate(points, start=0, end=15000)
    logger.info(f"Ranges = {min(sum(x) for x in ranges)}")
    sum_ranges = [sum(x) for x in ranges]
    sec = sum_ranges.index(min(sum(x) for x in ranges))
    logger.info(f"Seconds {sec}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
