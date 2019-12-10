from asyncio import Queue
import copy
import logging
import os

from year2019.utils import init_logging, run_main_coroutine
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)


async def main():
    program = read_program(os.path.join(
        os.path.dirname(__file__), "input.txt"))
    input = Queue()
    input.put_nowait(1)
    computer = Computer(copy.copy(program), input, Queue())
    await computer.execute()
    logger.info('Result part a: %s', computer.flush_output())
    input = Queue()
    input.put_nowait(2)
    computer = Computer(copy.copy(program), input, Queue())
    await computer.execute()
    logger.info('Result part b: %s', computer.flush_output())


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
