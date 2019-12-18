import logging
import copy
import os
from collections import deque, namedtuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input(test_n=None):
    graph = []
    if test_n is None:
        file_name = 'input.txt'
    else:
        file_name = 'test%d.txt' % test_n

    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        graph = [list(l) for l in f.readlines()]
        starting_pos = [(x, y) for y, line in enumerate(graph)
                        for x, c in enumerate(line) if c == '@'][0]
        return graph, starting_pos


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

State = namedtuple('State', 'pos keys')


def valid_pos(graph, pos, keys, MAX_X, MAX_Y):
    x, y = pos
    if x < 0 or x >= MAX_X or y < 0 or y >= MAX_Y:
        return False
    symbol = graph[y][x]
    if symbol == '#':
        return False
    if symbol.isupper() and symbol.lower() not in keys:
        return False
    return True


def bfs_with_states(graph, starting_pos):
    MAX_X = len(graph[0])
    MAX_Y = len(graph)
    ALL_KEYS = len([c for line in graph for c in line if c.islower()])
    que = deque()
    que.append((State(starting_pos, frozenset()), 0))
    seen_states = {}
    while len(que):
        state, depth = que.popleft()
        posns, keys = state.pos, state.keys
        if not all(valid_pos(graph, pos, keys, MAX_X, MAX_Y) for pos in posns):
            continue
        new_keys = set(keys)
        for x, y in posns:
            symbol = graph[y][x]
            if symbol.islower():
                new_keys.add(symbol)
        state = State(state.pos, frozenset(new_keys))
        if state in seen_states and seen_states[state] <= depth:
            continue

        seen_states[state] = depth
        if len(new_keys) == ALL_KEYS:
            continue
        for sq_id in range(len(posns)):
            for dx, dy in DIRECTIONS:
                new_posns = list(posns)
                new_posns[sq_id] = (new_posns[sq_id][0] + dx, new_posns[sq_id][1] + dy)
                new_posns = tuple(new_posns)
                new_state = State(new_posns, state.keys)
                que.append((new_state, depth + 1))
    states_with_all_keys = {
        k: v for k, v in seen_states.items() if len(k.keys) == ALL_KEYS}
    return min(v for v in states_with_all_keys.values())


def main():
    logger.info('Starting')
    # for i in range(1, 5):
    #     graph, starting_pos = read_input(test_n=i)
    #     res = bfs_with_states(graph, (starting_pos,))
    #     logger.info('Result for test %d is %d', i, res)
    # graph, starting_pos = read_input()
    # res = bfs_with_states(graph, (starting_pos, ))
    # logger.info('Result part a: %s', res)
    graph, starting_pos = read_input(test_n=5)
    x, y = starting_pos
    graph[y-1][x] = graph[y+1][x] = graph[y][x-1] = graph[y][x+1] = '#'
    res = bfs_with_states(graph, ((x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)))
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    main()
