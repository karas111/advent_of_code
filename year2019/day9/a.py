import copy
import logging
import os

from year2019.utils import init_logging
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [line for line in f]


def main():
    program = read_program(os.path.join(
        os.path.dirname(__file__), "input.txt"))
    input = [1]
    computer = Computer(copy.copy(program), input, [])
    computer.execute()
    logger.info('Result part a: %s', computer.output)
    input = [2]
    computer = Computer(copy.copy(program), input, [])
    computer.execute()
    logger.info('Result part b: %s', computer.output)


if __name__ == "__main__":
    init_logging()
    main()
