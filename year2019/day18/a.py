import logging
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
        return graph


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

State = namedtuple('State', 'posns keys')


def bfs(graph, starting_pos):
    MAX_X, MAX_Y = len(graph[0]), len(graph)
    que = deque()
    visited = set()
    que.append((starting_pos, 0, frozenset()))
    reacheable = {}
    while len(que):
        pos, depth, blocked_by = que.popleft()
        x, y = pos
        if x < 0 or x >= MAX_X or y < 0 or y >= MAX_Y:
            continue
        if pos in visited:
            continue
        symbol = graph[y][x]
        if symbol == '#':
            continue
        visited.add(pos)
        if symbol.islower():
            reacheable[pos] = (depth, blocked_by)
        new_blocked_by = blocked_by
        if symbol.isupper():
            new_blocked_by = blocked_by | frozenset([symbol.lower()])
        for dx, dy in DIRECTIONS:
            new_pos = (x + dx, y + dy)
            que.append((new_pos, depth+1, new_blocked_by))
    return reacheable


def reachable(graph, all_reachable, keys: frozenset):
    for (x, y), (depth, blocked_by) in all_reachable.items():
        symbol = graph[y][x]
        if symbol not in keys and keys.issuperset(blocked_by):
            yield ((x, y), depth)


def solve(graph):
    starting_positions = [(x, y) for y, line in enumerate(graph)
                          for x, c in enumerate(line) if c == '@']
    all_keys = [(x, y) for y, line in enumerate(graph)
                for x, c in enumerate(line) if c.islower()]
    key_graph = {}
    for pos in all_keys + starting_positions:
        key_graph[pos] = bfs(graph, pos)
    # logger.info(key_graph)

    que = deque()
    que.append((State(tuple(starting_positions), frozenset()), 0))
    seen_states = {}
    while len(que):
        # if len(seen_states) % 1000 == 0:
        #     logger.info('Seen states %d', len(seen_states))
        state, depth = que.popleft()
        new_keys = state.keys | frozenset(graph[y][x] for x, y, in state.posns)
        state = State(state.posns, new_keys)
        if state in seen_states and seen_states[state] <= depth:
            continue
        seen_states[state] = depth

        if len(new_keys) == len(all_keys) + 1:  # + 1 beacuse of @
            continue

        for idx, pos in enumerate(state.posns):
            for new_pos, path_len in reachable(graph, key_graph[pos], state.keys):
                new_posns = list(state.posns)
                new_posns[idx] = new_pos
                new_state = State(tuple(new_posns), state.keys)
                que.append((new_state, depth + path_len))
    states_with_all_keys = {
        k: v for k, v in seen_states.items() if len(k.keys) == len(all_keys) + 1}
    return min(states_with_all_keys.values())


def main():
    logger.info('Starting')
    # for i in range(5, 9):
    #     graph = read_input(test_n=i)
    #     res = solve(graph)
    #     logger.info('Result for test %d is %s', i, res)

    graph = read_input()
    res = solve(graph)
    logger.info('Result part a: %s', res)

    graph = read_input()
    x, y = [(x, y) for y, line in enumerate(graph)
            for x, c in enumerate(line) if c == '@'][0]
    graph[y-1][x] = graph[y+1][x] = graph[y][x -
                                             1] = graph[y][x+1] = graph[x][y] = '#'
    graph[y-1][x-1] = graph[y-1][x+1] = graph[y+1][x-1] = graph[y+1][x+1] = '@'
    res = solve(graph)
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    main()
