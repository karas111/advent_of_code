import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[tuple]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for r in f.readline().strip().split(","):
            s, e = map(int, r.split("-"))
            res.append((s, e))
        return res


def count_invalid_b(ranges: list[tuple], part_b: bool = False) -> list[int]:
    res = []
    for r in ranges:
        start, end = r
        start_str = str(start)
        if end < 10:
            continue

        seen = set()
        range_ = range(2, len(str(end)) + 1) if part_b else range(2, 3)
        for mult in range_:
            to_check_part = (
                int(start_str[: len(start_str) // mult])
                if len(start_str) // mult >= 1
                else 1
            )
            while True:
                to_check = int(str(to_check_part) * mult)
                to_check_part += 1
                if to_check < start:
                    continue
                elif to_check <= end:
                    seen.add(to_check)
                else:
                    break
        res.extend(seen)
    return res


def main():
    ranges = read_input()
    res = count_invalid_b(ranges, False)
    logger.info("Result a %d", sum(res))
    res = count_invalid_b(ranges, True)
    logger.info("Result b %d", sum(res))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
