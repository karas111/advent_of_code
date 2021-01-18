import logging
import time
from collections import deque
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class LinkedList:
    def __init__(self, value, right=None) -> None:
        self.value = value
        self.right = right


def spin_lock(skip_size, last_n):
    # last_n = 2017
    current = deque([0])
    for i in range(1, last_n + 1):
        current.rotate(-skip_size)
        current.append(i)
        if i % 10**6 == 0:
            logger.info(f"Instering {i}")
    return current


def part_b(skip_size, last_n):
    out = None
    curr_pos = 0
    tot_len = 1
    for i in range(1, last_n + 1):
        curr_pos = (curr_pos + skip_size) % tot_len
        curr_pos += 1
        if curr_pos == 1:
            out = i
        tot_len += 1
    return out


def main():
    skip_size = 337
    # skip_size = 3
    x = spin_lock(skip_size, last_n=2017)
    logger.info(f"Res A {x[0]}")
    # x = spin_lock(skip_size, last_n=50000000)
    # logger.info(f"Res B {x[x.index(0)+1]}")
    logger.info(f"Res B {part_b(skip_size, last_n=50000000)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
