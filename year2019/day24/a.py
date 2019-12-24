import copy
import logging
import os
from year2019.utils import init_logging, print_2darray

logger = logging.getLogger(__name__)


MAP_LEN = 5
MIDDLE_POS = MAP_LEN // 2
EMPTY_MAP = [[0]*MAP_LEN for _ in range(MAP_LEN)]


def read_input(test_n=None):
    if test_n is None:
        file_name = 'input.txt'
    else:
        file_name = 'test%d.txt' % test_n
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        res = [[c == '#' and 1 or 0 for c in line.strip()] for line in f]
    return res


def to_bitmask(map2d):
    bit_n = 0
    res = 0
    for row in map2d:
        for bit in row:
            res |= bit << bit_n
            bit_n += 1
    return res


def get_bug(map2d, row_id, col_id):
    if row_id < 0 or col_id < 0 or row_id >= MAP_LEN or col_id >= MAP_LEN:
        return 0
    return map2d[row_id][col_id]


def get_new_bit(old_bit, bugs_n):
    if old_bit == 1 and bugs_n != 1:
        return 0
    elif old_bit == 0 and bugs_n in [1, 2]:
        return 1
    return old_bit


def step_simulation(map2d):
    res = copy.deepcopy(map2d)
    for row_id, row in enumerate(map2d):
        for col_id, bit in enumerate(row):
            bugs_n = sum(get_bug(map2d, row_id + dx, col_id + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)])
            res[row_id][col_id] = get_new_bit(map2d[row_id][col_id], bugs_n)
    return res


def simulate_a(map2d):
    map2d = copy.deepcopy(map2d)
    visited = set([to_bitmask(map2d)])
    while True:
        map2d = step_simulation(map2d)
        bitmask = to_bitmask(map2d)
        if bitmask in visited:
            return bitmask
        visited.add(bitmask)


def get_bugs_b(map_with_levels, lvl, row_id, col_id):
    bugs_n = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        n_row, n_col = row_id + dx, col_id + dy
        if (lvl-1) in map_with_levels:
            if n_row == -1:
                bugs_n += map_with_levels[lvl-1][MIDDLE_POS-1][MIDDLE_POS]
            if n_row == MAP_LEN:
                bugs_n += map_with_levels[lvl-1][MIDDLE_POS+1][MIDDLE_POS]
            if n_col == -1:
                bugs_n += map_with_levels[lvl-1][MIDDLE_POS][MIDDLE_POS-1]
            if n_col == MAP_LEN:
                bugs_n += map_with_levels[lvl-1][MIDDLE_POS][MIDDLE_POS+1]
        if (lvl+1) in map_with_levels and n_row == MIDDLE_POS and n_col == MIDDLE_POS:
            if row_id == MIDDLE_POS - 1:
                bugs_n += sum(map_with_levels[lvl+1][0])
            if row_id == MIDDLE_POS + 1:
                bugs_n += sum(map_with_levels[lvl+1][MAP_LEN-1])
            if col_id == MIDDLE_POS - 1:
                bugs_n += sum(map_with_levels[lvl+1][i][0] for i in range(MAP_LEN))
            if col_id == MIDDLE_POS + 1:
                bugs_n += sum(map_with_levels[lvl+1][i][MAP_LEN-1] for i in range(MAP_LEN))
        if n_row not in [-1, MAP_LEN] and n_col not in [-1, MAP_LEN] and (n_row != MIDDLE_POS or n_col != MIDDLE_POS):
            bugs_n += map_with_levels[lvl][n_row][n_col]
    return bugs_n


def simulate_step_b(map_with_levels):
    res = copy.deepcopy(map_with_levels)
    for lvl, map2d in map_with_levels.items():
        for row_id, row in enumerate(map2d):
            for col_id, bit in enumerate(row):
                if row_id == MIDDLE_POS and col_id == MIDDLE_POS:
                    continue
                bugs_n = get_bugs_b(map_with_levels, lvl, row_id, col_id)
                res[lvl][row_id][col_id] = get_new_bit(bit, bugs_n)
    return res


def simulate_b(map2d, minutes=200):
    res = {0: map2d}
    for i in range(minutes):
        res[i+1] = copy.deepcopy(EMPTY_MAP)
        res[-i-1] = copy.deepcopy(EMPTY_MAP)
        res = simulate_step_b(res)
    return sum(sum(sum(row) for row in map2d) for map2d in res.values())


def main():
    logger.info('Starting...')
    map2d = read_input(test_n=None)
    res = simulate_a(map2d)
    logger.info('Result part a:\n%s', res)
    res = simulate_b(map2d, minutes=200)
    logger.info('Result part b:\n%s', res)

if __name__ == "__main__":
    init_logging()
    main()
