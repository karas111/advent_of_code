import logging
import os
import time
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Layer:
    def __init__(self, depth, l_range) -> None:
        self.depth = depth
        self.l_range = l_range

    def scanner_pos(self, delay):
        time = delay + self.depth
        offset = time % (2 * (self.l_range - 1))
        return offset if offset <= self.l_range - 1 else 2 * (self.l_range - 1) - offset

    def will_hit(self, delay):
        return self.scanner_pos(delay) == 0

    @property
    def severity(self):
        return self.depth * self.l_range

    def __repr__(self) -> str:
        return f"Layer{self.depth} <{self.l_range}>"


def parse_input():
    def parse_layer(line):
        depth, l_range = line.split(": ")
        return Layer(int(depth), int(l_range))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_layer(line.strip()) for line in f.readlines() if line]


def part_a(layers: List[Layer], delay=0):
    return [layer for layer in layers if layer.will_hit(delay)]


def part_b(layers):
    i = 0
    while True:
        if not any(layer.will_hit(i) for layer in layers):
            return i
        if i % 1000 == 0:
            logger.info(f"Delaying by {i}")
        i += 1


def main():
    layers = parse_input()
    caught = part_a(layers)
    logger.info(f"Res A {sum(layer.severity for layer in caught)}")
    logger.info(f"Res B {part_b(layers)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
