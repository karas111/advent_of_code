import logging
import os
import re
from collections import defaultdict

from numpy import delete
from traitlets import default

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def find_start(line: str, l: int = 4) -> int:
    has_multiple = set()
    occurences = defaultdict(lambda: 0)
    for idx, c in enumerate(line):
        occurences[c] += 1
        if occurences[c] == 2:
            has_multiple.add(c)
        if idx >= l:
            c_to_remove = line[idx - l]
            occurences[c_to_remove] -= 1
            if occurences[c_to_remove] == 1:
                has_multiple.remove(c_to_remove)
        if idx >= l - 1 and len(has_multiple) == 0:
            return idx + 1
    return -1


def main():
    line = read_input()
    idx = find_start(line)
    logger.info("Result a %s", idx)
    idx = find_start(line, l=14)
    logger.info("Result a %s", idx)


if __name__ == "__main__":
    init_logging()
    main()
