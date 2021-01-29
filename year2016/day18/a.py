import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        line = f.readline().strip()
        return parse_line(line)


def parse_line(line):
    return {(x, 0): 1 for x, c in enumerate(line) if c == "^"}, len(line)


def generate(traps, width, rows=40):
    for y in range(1, rows):
        for x in range(0, width):
            l, c, r = traps.get((x-1, y-1)), traps.get((x, y-1)), traps.get((x+1, y-1))
            if (l and c and not r) or (r and c and not l) or (l and not c and not r) or (r and not c and not l):
                traps[x, y] = 1
    return traps


def main():
    traps, width = parse_input()
    rows = 400000
    # traps, width = parse_line(".^^.^.^^^^")
    # rows = 10
    traps = generate(traps, width, rows)
    logger.info(f"Res A {rows * width - sum(traps.values())}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
