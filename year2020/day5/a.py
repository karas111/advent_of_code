import logging
import os
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def to_id(line):
    line = re.sub("F|L", "0", line)
    line = re.sub("B|R", "1", line)
    return int(line, 2)


def find_place(ids):
    ids = set(ids)
    missing_seats = set(range(2**10)) - ids
    for missing_id in missing_seats:
        if (missing_id + 1) in ids and (missing_id - 1) in ids:
            return missing_id


def main():
    lines = read_input()
    logger.info(to_id("FBFBBFFRLR"))
    ids = [to_id(line) for line in lines]
    logger.info(f"Result a {max(ids)}")
    logger.info(f"Result b {find_place(ids)}")


if __name__ == "__main__":
    init_logging()
    main()
