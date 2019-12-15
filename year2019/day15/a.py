from asyncio import Queue, gather, create_task
import copy
import logging
from collections import deque, namedtuple
import os

from year2019.utils import init_logging, run_main_coroutine
from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program

logger = logging.getLogger(__name__)

Node = namedtuple('Node', ['x', 'y', 'depth'])

DIRECTIONS = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

OPPOSITE_DIRECTION = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}

WALL = 0
SPACE = 1
OX_SYSTEM = 2


async def dfs(computer: Computer):
    stack = [((1, 0), 4)]
    graph = {}
    finished = set()
    while stack:
        pos, from_direction = stack[-1]
        if pos in graph:
            stack.pop()
            if pos not in finished:
                finished.add(pos)
                if graph[pos] in [SPACE, OX_SYSTEM]:
                    await computer.input.put(OPPOSITE_DIRECTION[from_direction])
                    await computer.output.get()
                continue

        await computer.input.put(from_direction)
        symbol = await computer.output.get()
        graph[pos] = symbol
        # logger.info('Looking at pos %s, symbol %s', pos, symbol)
        if symbol in [SPACE, OX_SYSTEM]:
            for direction, vec in DIRECTIONS.items():
                new_pos = (pos[0] + vec[0], pos[1] + vec[1])
                if new_pos in graph:
                    continue
                stack.append((new_pos, direction))
    return graph


def find_shortest(graph, starting_pos, stop_on_oxygen):
    que = deque([(starting_pos, 0)])
    visited = set()
    max_steps = None
    while len(que):
        pos, steps = que.popleft()
        if pos in visited:
            continue
        logger.info('Looking at %s, steps %s', pos, steps)
        visited.add(pos)
        symbol = graph[pos]
        max_steps = steps
        if symbol == OX_SYSTEM and stop_on_oxygen:
            return steps
        elif symbol == WALL:
            continue
        for vec in DIRECTIONS.values():
            new_pos = (pos[0] + vec[0], pos[1] + vec[1])
            que.append((new_pos, steps + 1))
    return max_steps


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    task = create_task(computer.execute())
    graph = await dfs(computer)
    logger.info('Graph: %s', graph)
    task.cancel()
    res = find_shortest(graph, starting_pos=(0, 0), stop_on_oxygen=True)
    logger.info('Result part a: %s', res)
    ox_pos = [pos for pos, v in graph.items() if v == OX_SYSTEM]
    res = find_shortest(graph, starting_pos=ox_pos[0], stop_on_oxygen=False)
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
