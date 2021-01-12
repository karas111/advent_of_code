import copy
import logging
import os
import time
from collections import Counter
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(line.strip()) for line in f.readlines() if line]


def part_a(jumps: List[int]) -> int:
    jumps_counter = 0
    idx = 0
    while 0 <= idx < len(jumps):
        didx = jumps[idx]
        jumps[idx] += 1
        idx += didx
        jumps_counter += 1
    return jumps_counter


def part_b(jumps: List[int]) -> int:
    jumps_counter = 0
    idx = 0
    while 0 <= idx < len(jumps):
        didx = jumps[idx]
        jumps[idx] += (didx >= 3 and -1 or 1)
        idx += didx
        jumps_counter += 1
    return jumps_counter


def main():
    jumps = parse_input()
    logger.info(f"Res A {part_a(copy.copy(jumps))}")
    logger.info(f"Res B {part_b(copy.copy(jumps))}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
