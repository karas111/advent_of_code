import logging
import os
import time
from sortedcontainers import SortedList

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    def parse_line(line):
        x, y = line.split("-")
        return (int(x), int(y))
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_line(line.strip()) for line in f.readlines() if line]


def connect_ranges(ranges):
    res = SortedList()
    for x, y in ranges:
        y += 1
        idx_left = res.bisect_left(x)
        idx_right = res.bisect_right(y)
        for to_remove in res[idx_left:idx_right]:
            res.remove(to_remove)
        if idx_left % 2 == 0:
            res.add(x)
        if idx_right % 2 == 0:
            res.add(y)
    return res


def main():
    ranges = parse_input()
    # ranges = [(5, 8), (0, 2), (4, 7)]
    sorted_ranges = connect_ranges(ranges)
    logger.info(f"Res A {sorted_ranges[1]}")
    tot_ips = 4294967295 + 1
    for x, y in zip(sorted_ranges[::2], sorted_ranges[1::2]):
        tot_ips -= y - x
    logger.info(f"Res B {tot_ips}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
