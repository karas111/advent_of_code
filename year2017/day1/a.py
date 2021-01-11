import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(x) for x in f.readline().strip()]


def part_a(c_list):
    filtered = [x for idx, x in enumerate(c_list) if x == c_list[(idx+1) % len(c_list)]]
    return sum(filtered)


def part_b(c_list):
    filtered = [x for idx, x in enumerate(c_list) if x == c_list[(idx+len(c_list)//2) % len(c_list)]]
    return sum(filtered)


def main():
    c_list = parse_input()
    logger.info(f"Res A {part_a(c_list)}")
    logger.info(f"Res A {part_b(c_list)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
