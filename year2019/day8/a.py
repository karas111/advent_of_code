import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for line in f:
            pass
    return input


def main():
    input = read_input()
    logger.info('Result')


if __name__ == "__main__":
    init_logging()
    main()
