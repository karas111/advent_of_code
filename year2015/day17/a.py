import logging
import os
from collections import defaultdict

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(line.strip()) for line in f]


def get_matching(cont: list[int], expected_size=150) -> int:
    res = defaultdict(int)
    for i in range(1 << len(cont)):
        size = sum(cont[bit] if (1 << bit) & i else 0 for bit in range(len(cont)))
        if size == expected_size:
            res[i.bit_count()] += 1
    return res


def main():
    conts = read_input()
    res = get_matching(conts)
    logger.info("Res a: %s", sum(res.values()))
    res_b = min(res.items())[1]
    logger.info("Res b: %s", res_b)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
