import copy
import logging
import os
import time

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


MOVE_VEC = [
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([0, 1]),
    np.array([-1, 0]),
]


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [(x[0], int(x[1:])) for x in f.readline().strip().split(", ")]


def main():
    pos = np.array([0, 0])
    direction = 0
    instructions = parse_input()
    visited = {(0, 0)}
    first_twice = None
    for inst in instructions:
        turn = inst[0] == "L" and -1 or 1
        direction = (direction + turn) % 4
        for _ in range(inst[1]):
            pos += MOVE_VEC[direction]
            if first_twice is None:
                if tuple(pos) in visited:
                    first_twice = copy.copy(pos)
                else:
                    visited.add(tuple(pos))
    logger.info(f"Res A {np.sum(np.abs(pos))}")
    logger.info(f"Res B {np.sum(np.abs(first_twice))}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
