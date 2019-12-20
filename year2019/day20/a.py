import logging
import copy
import os
from collections import namedtuple

from year2019.utils import init_logging, print_2darray

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "test1.txt")) as f:
        res = [list(line.strip('\n')) for line in f]
    res = [[' ', ' '] + line + [' ', ' '] for line in res]
    len_line = len(res[0])
    res = [[' '] * len_line]*2 + res + [[' '] * len_line]*2
    return res


Teleport = namedtuple('Teleport', ['label', 'entrace'])


def get_label(raw_graph, pos):
    x, y = pos
    symbol = raw_graph[y][x]
    if not symbol.isupper():
        return None
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (x + dx, y + dy)
        symbol_to_check = raw_graph[new_pos[1]][new_pos[0]]
        if symbol_to_check.isupper():
            sorted_cord = sorted([pos, new_pos])
            label = (raw_graph[sorted_cord[0][1]][sorted_cord[0][0]], raw_graph[sorted_cord[1][1]][sorted_cord[1][0]])
            for mult in [-1, 2]:
                entrace_pos = (x + dx * mult, y + dy * mult)
                if raw_graph[entrace_pos[1]][entrace_pos[0]] == '.':
                    return Teleport(label, entrace_pos)


def get_all_teleports(raw_graph):
    res = {}
    for y, line in enumerate(raw_graph):
        for x, _ in enumerate(line):
            tel = get_label(raw_graph, (x, y))
            if tel is not None:
                res[tel.entrace] = tel
    return res


def bfs_raw(raw_graph, pos):
    pass


def main():
    raw_graph = read_input()
    logger.info('Graph:\n%s', print_2darray(raw_graph))
    teleports = get_all_teleports(raw_graph)
    logger.info('Teleports:\n%s', teleports)
    res = None
    logger.info('Result part a: %s', res)
    res = None
    logger.info('Result part b: %s.', res)


if __name__ == "__main__":
    init_logging()
    main()
