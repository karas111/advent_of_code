import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [line for line in f]


def main():
    input = read_input()
    result = ''
    logger.info('Result:%s', str(result))


if __name__ == "__main__":
    init_logging()
    main()
