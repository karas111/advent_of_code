import copy
import logging
import os
from asyncio import Queue, gather

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, x, y, robot_direction):
        super().__init__()
        self.neighbours = []
        self.x = x
        self.y = y
        self.robot_direction = robot_direction

    def is_intersection(self):
        return len(self.neighbours) > 2

    def __repr__(self):
        return 'N(%d, %d)' % (self.x, self.y)


NEIGHB = [(1, 0), (-1, 0), (0, 1), (0, -1)]
ROBOT_DIECTIONS = {'^': 1, '>': 2, 'v': 3, '<': 4}


async def read_graph(computer: Computer):
    x, y = 0, 0
    graph = {}
    while not computer.finished or not computer.output.empty():
        symbol = await computer.output.get()
        symbol = chr(symbol)
        if symbol in ['#', '^', '<', '>', 'v']:
            node = Node(x, y, robot_direction=ROBOT_DIECTIONS.get(symbol))
            graph[(x, y)] = node
            for vect in NEIGHB:
                neighbour = graph.get((x + vect[0], y + vect[1]))
                if neighbour is not None:
                    neighbour.neighbours.append(node)
                    node.neighbours.append(neighbour)

        elif symbol == '\n':
            y += 1
            x = -1
        x += 1
    return graph


def find_intersections(graph):
    return sum(n.x * n.y for n in graph.values() if n.is_intersection())


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    graph, _ = await gather(read_graph(computer), computer.execute())
    res = find_intersections(graph)
    logger.info('Result part a: %s', res)
    res = None
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
