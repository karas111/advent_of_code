import itertools
import logging
import os
import time
from collections import deque
from typing import Deque, Tuple, List, Dict
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

def discrete_log(n, k, mod):
    res = 1
    i = 0
    while True:
        if res == n:
            return i
        res = (res * k) % mod
        i += 1


def main():
    key1, key2 = 17773298, 15530095
    # key1, key2 = 5764801, 17807724
    mod = 20201227
    loop_size1 = discrete_log(key1, 7, mod)
    encryption = pow(key2, loop_size1, mod)
    logger.info(f"Encryption {encryption}")
    


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
