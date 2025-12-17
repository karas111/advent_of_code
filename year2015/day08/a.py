import ast
import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def calculate_diff(w: str) -> int:
    return len(w) - len(ast.literal_eval(w))


def calculate_diff_b(w: str) -> int:
    return w.count("\\") + w.count('"') + 2


def main():
    words = read_input()
    logger.info("Res a: %s", sum(map(calculate_diff, words)))
    logger.info("Res a: %s", sum(map(calculate_diff_b, words)))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
