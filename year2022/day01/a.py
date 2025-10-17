import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_lists() -> list[list[int]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        groups = f.read().strip().split("\n\n")
        return [list(map(int, group.split("\n"))) for group in groups]


def main():
    groups = read_lists()
    callories = [sum(group) for group in groups]
    logger.info("Result a %d", max(callories))
    logger.info("Result b %d", sum(sorted(callories)[-3:]))


if __name__ == "__main__":
    init_logging()
    main()
