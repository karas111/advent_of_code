import logging
import copy
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [int(c) for c in f.readline()]


def main():
    input = read_input()
    res = None
    logger.info('Result part a: %s', res)
    res = None
    logger.info('Result part b: %s.', res)


if __name__ == "__main__":
    init_logging()
    main()
