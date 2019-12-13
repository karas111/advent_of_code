from asyncio import Queue, gather
import copy
import logging
import os

from year2019.utils import init_logging, run_main_coroutine
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)


EMPTY_I = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


async def create_game(computer):
    game = {}
    game_ready = False
    paddle_x, ball_x = None, None
    score = 0
    while not computer.finished or not computer.output.empty():
        x = await computer.output.get()
        y = await computer.output.get()
        item = await computer.output.get()
        if item in [BALL, PADDLE]:
            if item == BALL:
                ball_x = x
                if game_ready:
                    await computer.input.put(sign(ball_x-paddle_x))
                # logger.info('B(%d, %d)', x, y)
            if item == PADDLE:
                paddle_x = x
                # logger.info('P(%d, %d)', x, y)

        if x == -1 and y == 0:
            if not game_ready:
                game_ready = True
                await computer.input.put(sign(ball_x-paddle_x))
            score = item
            # logger.info('Score: %d', item)
        else:
            game[(x, y)] = item
        # if game_ready:
        #     print_game(game)

    return game, score


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
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    (game, _), _ = await gather(create_game(computer), computer.execute())
    logger.info('Result part a: %d', len([v for v in game.values() if v == 2]))
    program_mod = copy.copy(program)
    program_mod[0] = 2
    computer = Computer(program_mod, Queue(), Queue())
    (game, score), _ = await gather(create_game(computer), computer.execute())
    logger.info('Result part b: %d', score)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
