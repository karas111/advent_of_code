import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> tuple[list[list[int]], list[list[int]]]:
    keys, locks = [], []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for group in f.read().split("\n\n"):
            res = []
            for l in list(zip(*group.split("\n"))):
                res.append(l.count("#") - 1)
            if group[0][0] == ".":
                keys.append(res)
            else:
                locks.append(res)
    return keys, locks


def main():
    keys, locks = read_input()
    with catchtime(logger):
        res = 0
        for key in keys:
            for lock in locks:
                if all(k + l <= 5 for k, l in zip(key, lock)):
                    res += 1
        logger.info("Res A: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
