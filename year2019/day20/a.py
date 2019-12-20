import logging
import copy
import os
from collections import deque, namedtuple

from year2019.utils import init_logging, print_2darray

logger = logging.getLogger(__name__)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        res = [list(line.strip('\n')) for line in f]
    res = [[' ', ' '] + line + [' ', ' '] for line in res]
    len_line = len(res[0])
    res = [[' '] * len_line]*2 + res + [[' '] * len_line]*2
    return res


class Teleport:

    def __init__(self, lable, entrace, inner):
        self.label = lable
        self.entrace = entrace
        self.inner = inner
        self.other = None

    def __repr__(self):
        inner_s = self.inner and 'I' or 'O'
        return '%s%s%s' % (''.join(self.label), self.entrace, inner_s)


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_label(raw_graph, pos):
    MAX_X, MAX_Y = len(raw_graph[0]), len(raw_graph)
    OFFSET = 4
    x, y = pos
    symbol = raw_graph[y][x]
    if not symbol.isupper():
        return None
    for dx, dy in DIRECTIONS:
        new_pos = (x + dx, y + dy)
        symbol_to_check = raw_graph[new_pos[1]][new_pos[0]]
        if symbol_to_check.isupper():
            sorted_cord = sorted([pos, new_pos])
            label = (raw_graph[sorted_cord[0][1]][sorted_cord[0][0]], raw_graph[sorted_cord[1][1]][sorted_cord[1][0]])
            for mult in [-1, 2]:
                entrace_pos = (x + dx * mult, y + dy * mult)
                ex, ey = entrace_pos
                if raw_graph[ey][ex] == '.':
                    outer = ex == OFFSET or ey == OFFSET or ex == MAX_X - 1 - OFFSET or ey == MAX_Y - 1 - OFFSET
                    return Teleport(label, entrace_pos, not outer)


def get_all_teleports(raw_graph):
    res = {}
    label_to_teleport = {}
    for y, line in enumerate(raw_graph):
        for x, _ in enumerate(line):
            tel = get_label(raw_graph, (x, y))
            if tel is not None and tel.entrace not in res:
                res[tel.entrace] = tel
                other = label_to_teleport.get(tel.label)
                if other:
                    tel.other = other
                    other.other = tel
                else:
                    label_to_teleport[tel.label] = tel
    return res, label_to_teleport


def bfs_raw(raw_graph, starting_label, end_label, with_rec=False):
    teleports, label_to_tel = get_all_teleports(raw_graph)
    que = deque()
    que.append((label_to_tel[starting_label].entrace, 0, 0))
    res = {}
    visited = set()
    while len(que):
        pos, depth, maze_lvl = que.popleft()
        if not with_rec:
            maze_lvl = 0
        x, y = pos
        symbol = raw_graph[y][x]
        if symbol != '.':
            continue
        if maze_lvl < 0:
            continue
        vis_key = (pos, maze_lvl)
        if vis_key in visited:
            continue
        visited.add(vis_key)
        tel = teleports.get(pos)
        if tel:
            res[(''.join(tel.label), tel.inner, maze_lvl)] = depth
            if tel.label == end_label and maze_lvl == 0:
                return res
            if tel.other:
                lvl_dx = tel.inner and 1 or -1
                que.append((tel.other.entrace, depth+1, maze_lvl + lvl_dx))
        for dx, dy in DIRECTIONS:
            n_pos = (x + dx, y + dy)
            que.append((n_pos, depth+1, maze_lvl))


def main():
    raw_graph = read_input()
    res = bfs_raw(raw_graph, ('A', 'A'), ('Z', 'Z'))
    # logger.info('Depths: %s', res)
    logger.info('Result part a: %s', res[('ZZ', False, 0)])
    res = bfs_raw(raw_graph, ('A', 'A'), ('Z', 'Z'), with_rec=True)
    # logger.info('Depths: %s', res)
    logger.info('Result part b: %s', res[('ZZ', False, 0)])


if __name__ == "__main__":
    init_logging()
    main()
