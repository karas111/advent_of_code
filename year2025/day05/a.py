import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> tuple[list[range], list[int]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        ranges = []
        for line in f:
            line = line.strip()
            if not line:
                break
            ranges.append(tuple(map(int, line.split("-"))))
        ranges = [range(a, b + 1) for a, b in ranges]
        idxs = [int(line.strip()) for line in f]
        return ranges, idxs


def solve_a(ranges, idxs):
    res = 0
    for idx in idxs:
        # can be done better - sort ranges, merge overllaping
        # and do binary search
        res += any(idx in range_ for range_ in ranges)
    return res


def solve_b(ranges: list[range]) -> int:
    ranges = [(r.start, r.stop) for r in ranges]
    ranges = sorted(ranges)
    last_end = -1
    res = 0
    for start, end in ranges:
        start = max(start, last_end)
        end = max(end, last_end)
        last_end = end
        res += end - start
    return res


def main():
    ranges, idxs = read_input()
    res = solve_a(ranges, idxs)
    logger.info("Result a %s", res)
    res = solve_b(ranges)
    logger.info("Result b %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
