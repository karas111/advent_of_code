import copy
import logging
import os
from asyncio import Queue, gather

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine

logger = logging.getLogger(__name__)


async def part1(computer: Computer):
    return None


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    res, _ = gather(part1(computer), computer.execute())
    logger.info('Result part a: %s', res)
    res = None
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
