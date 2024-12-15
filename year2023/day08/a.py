import logging
import os
import re
from math import lcm

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Graph = dict[str, tuple[str, str]]


def read_input() -> tuple[str, Graph]:
    g = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        moves = f.readline().strip()
        f.readline()
        pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
        for line in f:
            source, left, right = re.match(pattern, line).groups()
            g[source] = (left, right)
        return moves, g


def move(g: Graph, moves: str, start: str = "AAA", end: str = "ZZZ") -> int:
    steps = 0
    current = start
    while current != end:
        direction = moves[steps % len(moves)]
        if direction == "L":
            current = g[current][0]
        else:
            current = g[current][1]
        steps += 1
        if current.endswith(end):
            return steps
    return steps


def main():
    moves, g = read_input()
    with catchtime(logger):
        res = move(g, moves)
        logger.info("Res A: %s", res)

        starting = [s for s in g if s.endswith("Z")]
        steps = [move(g, moves, start=s, end="Z") for s in starting]
        logger.info("Res B %s", lcm(*steps))


if __name__ == "__main__":
    init_logging()
    main()
