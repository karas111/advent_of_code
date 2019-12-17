import copy
import logging
import os
from asyncio import Queue, gather
from collections import namedtuple

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, print_2dgraph, run_main_coroutine

logger = logging.getLogger(__name__)

DIRECTION_MAPPING = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}
ROBOT_DIECTIONS = {'^': 0, '>': 1, 'v': 2, '<': 3}
REV_ROBOT_DIRECTIONS = {v: k for k, v in ROBOT_DIECTIONS.items()}


class Robot:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


async def read_graph(computer: Computer):
    x, y = 0, 0
    graph = {}
    robot = None
    while not computer.finished or not computer.output.empty():
        symbol = await computer.output.get()
        symbol = chr(symbol)
        if symbol in '#^<>v':
            if symbol != '#':
                robot = Robot(x, y, ROBOT_DIECTIONS.get(symbol))
            graph[(x, y)] = 0

            for vect in DIRECTION_MAPPING.values():
                n_pos = (x + vect[0], y + vect[1])
                if n_pos in graph:
                    graph[n_pos] += 1
                    graph[(x, y)] += 1

        elif symbol == '\n':
            y += 1
            x = -1
        x += 1
    return graph, robot


def find_intersections(graph):
    return sum(x * y for (x, y), degree in graph.items() if degree > 2)


def log_graph(graph, robot):
    new_graph = copy.copy(graph)
    new_graph[(robot.x, robot.y)] = REV_ROBOT_DIRECTIONS[robot.direction]
    logger.info('Graph:\n%s', print_2dgraph(new_graph))


def nromalize_path(path):
    path = [str(c) for c in path if c != 0]
    path = ''.join(path)
    path = path.replace('RRR', 'L')
    return path


def generate_path(graph, robot):
    path = []
    counter = 0
    last_move_forward_dir = None
    visited = set([(robot.x, robot.y)])
    while len(visited) < len(graph):
        vec = DIRECTION_MAPPING[robot.direction]
        new_pos = (robot.x + vec[0], robot.y + vec[1])
        if new_pos in graph and last_move_forward_dir != (robot.direction + 2) % 4:
            # if counter == 0 and path:
            #     log_graph(graph, robot)
            #     logger.info('Path: %s', nromalize_path(path))
            visited.add(new_pos)
            last_move_forward_dir = robot.direction
            counter += 1
            robot.x = new_pos[0]
            robot.y = new_pos[1]
        else:
            path.append(counter)
            path.append('R')
            robot.direction = (robot.direction + 1) % 4
            counter = 0
    path.append(counter)
    log_graph(graph, robot)
    logger.info('Path: %s', nromalize_path(path))
    return nromalize_path(path)


async def part_b(graph, robot, computer: Computer):
    path = generate_path(graph, robot)
    main = 'A,B,A,C,A,B,C,B,C,B'
    lines = [
        main,
        'L,10,R,8,L,6,R,6',
        'L,8,L,8,R,8',
        'R,8,L,6,L,10,L,10',
        'n'
    ]
    for line in lines:
        for c in line:
            await computer.input.put(ord(c))
        await computer.input.put(ord('\n'))
    return None
    return await computer.flush_output


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(
        os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    (graph, robot), _ = await gather(read_graph(computer), computer.execute())
    res = find_intersections(graph)
    logger.info('Result part a: %s', res)
    log_graph(graph, robot)
    new_prog = copy.copy(program)
    new_prog[0] = 2
    computer = Computer(new_prog, Queue(), Queue())
    res, _ = await gather(part_b(graph, robot, computer), computer.execute())
    logger.info('Result part b: %s', computer.flush_output()[-1])


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
