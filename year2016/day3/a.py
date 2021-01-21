import logging
import os
import time

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [
            [int(x) for x in line.strip().split()] for line in f.readlines() if line
        ]


def is_triangle(sides):
    sides = list(sorted(sides))
    return sides[2] < sum(sides[:2])


def main():
    all_sides = parse_input()
    triangles = [is_triangle(sides) for sides in all_sides]
    logger.info(f"Res A {sum(triangles)}")
    all_sides = np.array(all_sides).flatten("F")
    all_sides = np.array_split(all_sides, len(all_sides) // 3)
    triangles = [is_triangle(sides) for sides in all_sides]
    logger.info(f"Res B {sum(triangles)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
