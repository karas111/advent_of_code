import logging
import os
import re
import time
from collections import namedtuple

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Point = namedtuple("Point", ["pos", "vel", "acc"])


def step(point):
    new_vel = point.vel + point.acc
    new_pos = point.pos + new_vel
    return point._replace(vel=new_vel, pos=new_pos)


def parse_input():
    def parse_point(line) -> Point:
        data = re.match("p=<(.*)>, v=<(.*)>, a=<(.*)>", line).groups()
        data = [
            np.array([int(coord.strip()) for coord in coords.split(",")])
            for coords in data
        ]
        return Point(*data)

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_point(line.strip()) for line in f.readlines() if line]


def distance(coords):
    return sum(np.abs(coords))


def main():
    points = parse_input()
    min_point = min(enumerate(points), key=lambda p: distance(p[1].acc))
    logger.info(f"Res A {min_point[0]}")
    points = dict(enumerate(points))
    for j in range(10 ** 3):
        new_points = {i: step(point) for i, point in points.items()}
        posns_dict = {}
        for i, point in new_points.items():
            posns_dict.setdefault(tuple(point.pos), []).append(i)
        collisions = [x for x in posns_dict.values() if len(x) > 1]
        collisions = {y for x in collisions for y in x}
        points = {i: p for i, p in new_points.items() if i not in collisions}
        if j % 10 == 0:
            logger.info(f"simulation step {j}. Left {len(points)}")
    logger.info(f"Res B {len(points)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
