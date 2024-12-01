import os
import logging
import re
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_lists() -> tuple[list[int], list[int]]:
    pattern = re.compile(r"^(\d+)\s+(\d+)$")
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        l = [pattern.match(line.strip()).groups() for line in f]
    l = [(int(x), int(y)) for x, y in l]
    return list(zip(*l))


def calculate_similarity(l1: list[int], l2: list[int]):
    res = [x * l2.count(x) for x in l1]
    return sum(res)


def main():
    l1, l2 = [sorted(l) for l in read_lists()]
    distances= [abs(x - y) for x, y in zip(l1, l2)]
    logger.info(f"Result a {sum(distances)}")
    logger.info(f"Result a {calculate_similarity(l1, l2)}")
    


if __name__ == "__main__":
    init_logging()
    main()
