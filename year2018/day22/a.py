import logging
import time
from enum import Enum
from heapdict import heapdict
from year2019.utils import init_logging


logger = logging.getLogger(__name__)


class Equipment(Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING = 2


def get_allowed_eq(region):
    return [x for x in Equipment if x.value != region]


def get_terrain_type(depth, target, size):
    mod1, mod2 = 20183, 3
    gi_index = [[0] * (size[0]) for _ in range(size[1])]
    er_lvl = [[0] * (size[0]) for _ in range(size[1])]
    # res[0][0] = 0
    for y, row in enumerate(gi_index):
        for x in range(len(row)):
            if x == 0 and y == 0:
                gi_index[y][x] = 0
            elif (x, y) == target:
                gi_index[y][x] = 0
            elif y == 0:
                gi_index[y][x] = x * 16807
            elif x == 0:
                gi_index[y][x] = y * 48271
            else:
                gi_index[y][x] = er_lvl[y-1][x] * er_lvl[y][x-1]
            er_lvl[y][x] = (gi_index[y][x] + depth) % mod1
    res = [[er % mod2 for er in line] for line in er_lvl]
    return res


def dijkstra(grid, destination):
    queue = heapdict()
    res = {}
    for y, line in enumerate(grid):
        for x in range(len(line)):
            for eq in Equipment:
                key = ((x, y), eq)
                queue[key] = float('inf')
                res[key] = (None, float('inf'))
    queue[((0, 0), Equipment.TORCH)] = 0
    while len(queue):
        ((x, y), eq), priority = queue.popitem()
        if (x, y) == destination and eq == Equipment.TORCH:
            return res
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and eq in get_allowed_eq(grid[ny][nx]):
                key = ((nx, ny), eq)
                if key in queue and queue[key] > priority + 1:
                    queue[key] = priority + 1
                    res[key] = (((x, y), eq), priority + 1)
        for neq in Equipment:
            if neq != eq and neq in get_allowed_eq(grid[y][x]):
                key = ((x, y), neq)
                if key in queue and queue[key] > priority + 7:
                    queue[key] = priority + 7
                    res[key] = (((x, y), eq), priority + 7)


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    depth, target = 4845, (6, 770)
    # depth, target = 510, (10, 10)
    terrain_type = get_terrain_type(depth, target, (target[0] + 1, target[1] + 1))

    logger.info(f"Res A {sum(sum(line) for line in terrain_type)}")
    terrain_type = get_terrain_type(depth, target, (target[0] + 100, target[1] + 100))
    res_b = dijkstra(terrain_type, target)
    logging.info(f"Res B {res_b[(target, Equipment.TORCH)][1]}")

    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
