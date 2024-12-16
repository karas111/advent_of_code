import logging
import os
from collections import deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


SYMBOL_TO_VECS = {
    "-": [Cords(1, 0), Cords(-1, 0)],
    "|": [Cords(0, 1), Cords(0, -1)],
    "7": [Cords(-1, 0), Cords(0, 1)],
    "J": [Cords(-1, 0), Cords(0, -1)],
    "L": [Cords(1, 0), Cords(0, -1)],
    "F": [Cords(1, 0), Cords(0, 1)],
}
S_MAP = "J"


Grid = list[str]


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def find_node(g: Grid, c: str) -> Cords:
    for y, line in enumerate(g):
        for x, cc in enumerate(line):
            if c == cc:
                return Cords(x, y)


def bfs(g: Grid, start: Cords) -> int:
    visited = set()
    queue = deque([(start, 0)])
    depths = {}
    while queue:
        current, depth = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        depths[current] = depth
        symbol = g[current.y][current.x]
        if symbol == "S":
            symbol = S_MAP
        for dv in SYMBOL_TO_VECS[symbol]:
            neighbour = dv + current
            queue.append((neighbour, depth + 1))
    return max(depths.values()), visited


def calculate_inner_nodes(g: Grid, loop: set[Cords]):
    inner_nodes = 0
    enclosed = False
    for y, line in enumerate(g):
        last_opening_turn = None
        for (
            x,
            c,
        ) in enumerate(line):
            if c == "S":
                c = S_MAP
            cords = Cords(x, y)
            if cords in loop:
                if c == "|":
                    enclosed = not enclosed
                elif c in "FL":
                    last_opening_turn = c
                elif c in "J7":
                    if last_opening_turn + c in ("FJ", "L7"):
                        enclosed = not enclosed
                    last_opening_turn = None
            else:
                inner_nodes += enclosed
    return inner_nodes


def main():
    g = read_input()
    with catchtime(logger):
        max_depth, loop = bfs(g, find_node(g, "S"))
        logger.info("Res A: %s", max_depth)
        inner_nodes = calculate_inner_nodes(g, loop)
        logger.info("Res B: %s", inner_nodes)


if __name__ == "__main__":
    init_logging()
    main()
