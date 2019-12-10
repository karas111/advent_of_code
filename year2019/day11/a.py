import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [n for n in f.readline().strip()]


def main():
    raw_data = read_input()
    res_a = None
    logger.info('Result part a: %s', res_a)
    res_b = None
    logger.info('Result part b: %s', res_b)


if __name__ == "__main__":
    init_logging()
    main()
