import logging
import os
import re

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return list(map(lambda l: l.strip(), f))


def is_matching(w: str) -> bool:
    pattern = r"^(?=(?:.*[aeiou]){3,})(?=.*([a-z])\1)(?!.*(?:ab|cd|pq|xy))[a-z]+$"
    return re.match(pattern, w) is not None


def is_matching_b(w: str) -> bool:
    pattern = r"^(?=.*([a-z]{2}).*\1)(?=.*([a-z]).\2)[a-z]+$"
    return re.match(pattern, w) is not None


def main():
    words = read_input()
    matching_w = list(filter(is_matching, words))
    logger.info("Res a: %d", len(matching_w))
    matching_w = list(filter(is_matching_b, words))
    logger.info("Res b: %d", len(matching_w))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
