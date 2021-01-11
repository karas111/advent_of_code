import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

VECTORS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def find_pos(idx):
    current_idx = 0
    x, y = 0, 0
    side = 1
    vec_idx = 0
    while current_idx < idx:
        move = min(side, idx - current_idx)
        dvec = tuple(cord * move for cord in VECTORS[vec_idx])
        x += dvec[1]
        y += dvec[0]
        current_idx += side
        vec_idx = (vec_idx + 1) % 4
        if vec_idx % 2 == 0:
            side += 1
    return x, y


def init_mem(idx):
    current_idx = 0
    x, y = 0, 0
    side = 1
    vec_idx = 0
    res = {(0, 0): 1}
    while current_idx < idx:
        move = min(side, idx - current_idx)
        for i in range(move):
            x += VECTORS[vec_idx][1]
            y += VECTORS[vec_idx][0]
            if x != 0 or y != 0:
                val = sum(res.get((x+dx, y+dy), 0) for dx in range(-1, 2) for dy in range(-1, 2) if dx != 0 or dy != 0)
                res[(x, y)] = val
                if val > idx:
                    return val
        current_idx += side
        vec_idx = (vec_idx + 1) % 4
        if vec_idx % 2 == 0:
            side += 1
    return res


def main():
    idx = 289326
    # idx = 23
    res_a = find_pos(idx-1)
    logger.info(f"Res A {res_a}, {sum(abs(x) for x in res_a)}")
    res_b = init_mem(idx-1)
    logger.info(f"Res B {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
