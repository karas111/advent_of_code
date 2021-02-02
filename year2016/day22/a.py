import logging
import os
import time
import re
from collections import deque, namedtuple
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Node = namedtuple("Node", ["x", "y", "size", "used", "avail", "use_pct"])


def parse_input():
    def parse_node(line):
        match = re.match(r"/dev/grid/node-x(\d+)-y(\d+)\s*(\d+)T\s*(\d+)T\s*(\d+)T\s*(\d+)%", line)
        return Node(*[int(arg) for arg in match.groups()])

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_node(line.strip()) for line in f.readlines()[2:] if line]


def calculate_a(nodes):
    count = 0
    for node in nodes:
        for other in nodes:
            if node != other and node.used != 0 and other.avail >= node.used:
                count += 1
    return count


def print_nodes(nodes):
    x, y = max(n.x for n in nodes) + 1, max(n.y for n in nodes) + 1
    grid = [["."] * x for _ in range(y)]
    for node in nodes:
        c = 'x'
        if node.used > 100:
            c = "#"
        elif node.used == 0:
            c = "_"
        grid[node.y][node.x] = c
    grid_str = "\n".join(["".join(line) for line in grid])
    logger.info(f"\n{grid_str}")


def main():
    nodes = parse_input()
    logger.info(f"Res A {calculate_a(nodes)}")
    print_nodes(nodes)


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
