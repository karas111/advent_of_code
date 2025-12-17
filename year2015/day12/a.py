import json
import logging
import os
import re

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def all_numbers(line: str) -> list[int]:
    return list(map(int, re.findall(r"-?\d+", line)))


def part_b(line: str) -> int:
    parse = json.loads(line)

    def sum_ints(obj) -> int:
        if isinstance(obj, int):
            return obj
        elif isinstance(obj, list):
            return sum(map(sum_ints, obj))
        elif isinstance(obj, dict):
            vals = list(obj.values())
            if "red" in vals:
                return 0
            else:
                return sum(map(sum_ints, vals))
        return 0

    return sum_ints(parse)


def main():
    line = read_input()
    logger.info("Res a: %d", sum(all_numbers(line)))
    logger.info("Res b: %d", part_b(line))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
