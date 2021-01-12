import copy
import logging
import os
import time
from collections import Counter
from typing import Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return tuple(int(x) for x in f.readline().strip().split("\t"))


def cycle_once(blocks: Tuple[int]) -> Tuple[int]:
    idx_start = blocks.index(max(blocks))
    to_split = blocks[idx_start]
    n_blocks = list(blocks)
    n_blocks[idx_start] = 0
    n_blocks = [x + to_split // len(blocks) for x in n_blocks]
    for i in range(idx_start + 1, idx_start + 1 + to_split % len(blocks)):
        n_blocks[i % len(blocks)] += 1
    return tuple(n_blocks)


def part_a_b(blocks: Tuple[int]) -> int:
    cycles = 0
    seen_states = {}
    while blocks not in seen_states:
        seen_states[blocks] = cycles
        blocks = cycle_once(blocks)
        cycles += 1
    return cycles, cycles - seen_states[blocks]


def main():
    blocks = parse_input()
    # blocks = (0, 2, 7, 0)
    logger.info(f"Res A {part_a_b(blocks)}")
    # logger.info(f"Res B {ju}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
