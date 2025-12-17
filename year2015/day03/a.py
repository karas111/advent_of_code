import logging
import os

import catch_time
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


MOVES = {">": Cords(1, 0), "v": Cords(0, 1), "<": Cords(-1, 0), "^": Cords(0, -1)}


def main():
    path = read_input()
    current = Cords(0, 0)
    seen = {current}
    for c in path:
        current = current + MOVES[c]
        seen.add(current)
    logger.info("Result a %d", len(seen))

    current = [Cords(0, 0), Cords(0, 0)]
    i = 0
    seen = {current[0]}
    for c in path:
        current[i] = current[i] + MOVES[c]
        seen.add(current[i])
        i = (i + 1) % 2
    logger.info("Result b %d", len(seen))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
