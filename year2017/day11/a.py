import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


MOVE_VEC = {
    "n": (0, -1),
    "s": (0, 1),
    "se": (1, 0),
    "nw": (-1, 0),
    "ne": (1, -1),
    "sw": (-1, 1),
}


def parse_input(part_b=False):
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip().split(",")


def move_directions(directions):
    x, y = 0, 0
    max_dist = 0
    for direction in directions:
        x += MOVE_VEC[direction][0]
        y += MOVE_VEC[direction][1]
        max_dist = max(max_dist, manhattan_hex(x, y))
    return x, y, max_dist


def manhattan_hex(dx, dy):
    if dx * dy >= 0:
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))


def main():
    directions = parse_input()
    # directions = "ne,ne,s,s".split(",")
    dx, dy, max_dist = move_directions(directions)
    dist = manhattan_hex(dx, dy)
    logger.info(f"Res A {dist}, Res B {max_dist}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
