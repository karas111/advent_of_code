from asyncio import Queue, gather
import copy
import logging
import os

from year2019.utils import init_logging, run_main_coroutine
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)


async def create_game(computer):
    game = {}
    game_ready = False
    while not computer.finished or not computer.output.empty():
        x = await computer.output.get()
        y = await computer.output.get()
        item = await computer.output.get()
        if x == -1 and y == 0:
            game_ready = True
            await computer.input.put(0)
            logger.info('Score P(%d, %d): %d', x, y, item)
        else:
            game[(x, y)] = item
        if game_ready:
            print_game(game)

    return game


EMPTY_I = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


def print_game(game):
    max_x, max_y = max(x for x, _ in game), max(y for _, y in game)
    res = []
    c_map = {
        EMPTY_I: ' ',
        WALL: '|',
        BLOCK: '#',
        PADDLE: '-',
        BALL: 'o'
    }
    for y in range(max_y+1):
        line = [c_map[game.get((x, y), 0)] for x in range(max_x + 1)]
        res.append(''.join(line))
    logger.info('Game:\n%s', '\n'.join(res))


async def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    game, _ = await gather(create_game(computer), computer.execute())
    logging.info('Result part a: %d', len([v for v in game.values() if v == 2]))
    program_mod = copy.copy(program)
    program_mod[0] = 2
    computer = Computer(program_mod, Queue(), Queue())
    game, _ = await gather(create_game(computer), computer.execute())


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
