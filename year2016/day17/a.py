import logging
import time
from collections import deque
from hashlib import md5
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

PATH_VEC = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def bfs(x, y, seed):
    dest = (3, 3)
    queue = deque([(0, 0, "")])
    all_paths = []
    while queue:
        x, y, path = queue.popleft()
        if (x, y) == dest:
            all_paths.append(path)
            continue
        path_hash = md5(f"{seed}{path}".encode()).hexdigest()
        for hash_c, (path_c, (dx, dy)) in zip(path_hash[:4], PATH_VEC.items()):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 4 and 0 <= ny < 4 and hash_c in "bcdef":
                queue.append((nx, ny, path + path_c))
    return all_paths


def main():
    seed = "veumntbg"
    # seed = "ulqzkmiv"
    res_a = bfs(0, 0, seed)
    logger.info(f"Res A {res_a[0]}")
    logger.info(f"Res B {len(res_a[-1])}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
