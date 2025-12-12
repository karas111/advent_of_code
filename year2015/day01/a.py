import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def main():
    line = read_input()
    logger.info("Result a %d", line.count("(") - line.count(")"))

    floor = 0
    for idx, c in enumerate(line):
        floor += (c == "(") - (c == ")")
        if floor < 0:
            logger.info("result b: %d", idx + 1)
            break


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
