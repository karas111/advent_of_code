from asyncio import Queue, gather
import copy
import logging
import os

import numpy
from PIL import Image

from year2019.utils import init_logging, run_main_coroutine
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)


def modify_directoin(direction, mod):
    if mod == 0:
        return (direction - 1) % 4
    elif mod == 1:
        return (direction + 1) % 4


def move_ship(pos, direction):
    move_v = {
        0: (-1, 0),
        1: (0, 1),
        2: (1, 0),
        3: (0, -1)
    }
    return (pos[0] + move_v[direction][0], pos[1] + move_v[direction][1])


async def count_painted(computer: Computer, initial_color):
    ship = {}
    pos = (0, 0)
    ship[pos] = initial_color
    direction = 0
    while not computer.finished:
        await computer.input.put(ship.get(pos, 0))
        paint = await computer.output.get()
        ship[pos] = paint
        # logger.info('Painted %s with %d', pos, paint)
        dir_mod = await computer.output.get()
        direction = modify_directoin(direction, dir_mod)
        pos = move_ship(pos, direction)
        # logger.info('Moving to %s', pos)
    return ship


def paint_ship(ship):
    white_coordinates = [cor for cor, val in ship.items() if val == 1]
    min_x, min_y = min(x for x, y in white_coordinates), min(y for x, y in white_coordinates)
    white_coordinates = [(x + min_x, y + min_y) for x, y in white_coordinates]
    data = numpy.zeros((32, 64, 3), dtype=numpy.uint8)
    for cord in white_coordinates:
        data[cord[0], cord[1]] = [255, 255, 255]
    image = Image.fromarray(data)
    image.show()


async def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    input = Queue()
    computer = Computer(copy.copy(program), input, Queue())
    ship, _ = await gather(count_painted(computer, initial_color=0), computer.execute())
    logger.info('Result part a: %s', len(ship))
    computer = Computer(copy.copy(program), input, Queue())
    ship, _ = await gather(count_painted(computer, initial_color=1), computer.execute())
    paint_ship(ship)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
