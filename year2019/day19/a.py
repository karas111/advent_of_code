import copy
import logging
import os
from asyncio import Queue, gather, create_task
from collections import namedtuple

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, print_2dgraph, run_main_coroutine

logger = logging.getLogger(__name__)


async def read_graph(program, max_x, max_y):
    result = []
    for i in range(max_y):
        line = []
        for j in range(max_x):
            computer = Computer(copy.copy(program), Queue(), Queue())
            await computer.input.put(j)
            await computer.input.put(i)
            await computer.execute()
            symbol = await computer.output.get()
            line.append(symbol)
        result.append(line)
    return result


async def check_point(program, x, y):
    if x < 0 or y < 0:
        return False
    computer = Computer(copy.copy(program), Queue(), Queue())
    await computer.input.put(x)
    await computer.input.put(y)
    await computer.execute()
    symbol = await computer.output.get()
    return bool(symbol)


# async def fits(program, x, y, n):
#     to_check = [(x-n, y-n), (x+n, y-n)]
#     for n_x, n_y in to_check:
#         if not await check_point(program, n_x, n_y):
#             return False
#     return True


async def find_big(program, n=100):
    x = y = 0
    while not await check_point(program, x-n, y+n):
        x += 1
        while not await check_point(program, x, y):
            y += 1
        if x % 100 == 0:
            logger.info('TR(%d, %d)', x, y)
    return (x-n, y)


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    # graph = await read_graph(program, 50, 50)
    # logger.info('Result part a: %s', sum(sum(line) for line in graph))
    # logger.info('Beam\n%s', '\n'.join(''.join(c and '#' or ' ' for c in line) for line in graph))
    res = await find_big(program)
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
