import asyncio
import copy
import logging
import os

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine


async def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    input = asyncio.Queue()
    input.put_nowait(1)
    computer = Computer(copy.copy(program), input, asyncio.Queue())
    await computer.execute()
    logging.info('Result for part a: %s', computer.flush_output())
    input = asyncio.Queue()
    input.put_nowait(5)
    computer = Computer(copy.copy(program), input, asyncio.Queue())
    await computer.execute()
    logging.info('Result for part b: %s', computer.flush_output())


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
