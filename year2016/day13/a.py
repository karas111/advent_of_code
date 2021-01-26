import logging
import time
from collections import deque
import itertools

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

MAGIC_NUMBER = 1352
# MAGIC_NUMBER = 10


def is_space(x, y):
    number = x*x + 3*x + 2*x*y + y + y*y + MAGIC_NUMBER
    return bin(number).count("1") % 2 == 0


def bfs(x, y, max_steps):
    seen_pos = {}
    queue = deque([(x, y, 0)])
    while queue:
        x, y, steps = queue.popleft()
        if (x, y) in seen_pos:
            continue
        seen_pos[(x, y)] = steps
        if steps > max_steps:
            continue
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n_x, n_y = x + dx, y + dy
            if n_x < 0 or n_y < 0:
                continue
            if is_space(n_x, n_y):
                queue.append((n_x, n_y, steps+1))
    return seen_pos


def main():
    # res_a = bfs(1, 1, 7, 4)
    res = bfs(1, 1, max_steps=100)
    logger.info(f"Res A {res[(31, 39)]}")
    logger.info(f"Res A {len([x for x in res.values() if x <= 50])}")

if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
