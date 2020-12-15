import logging
import math
import os
import re
import time
from collections import namedtuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

TEST1 = [0, 3, 6]
TEST2 = [1, 3, 2]
TEST3 = [1, 2, 3]


def play(start_numbers, max_rounds=2020):
    occurences = {n: idx for idx, n in enumerate(start_numbers)}
    last_n = start_numbers[-1]
    for i in range(len(start_numbers), max_rounds):
        if last_n in occurences:
            new_last_n = i - 1 - occurences.get(last_n, 0)
        else:
            new_last_n = 0
        occurences[last_n] = i - 1
        last_n = new_last_n
    return last_n


def main():
    start_numbers = [16, 12, 1, 0, 15, 7, 11]
    # start_numbers = TEST2
    res = play(start_numbers)
    logger.info(f"Res A={res}")
    res = play(start_numbers, max_rounds=30000000)
    logger.info(f"Res A={res}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
