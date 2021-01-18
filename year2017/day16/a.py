import logging
import os
import time
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Move:
    def dance(self, programs):
        raise NotImplementedError()


class Spin(Move):
    def __init__(self, spin) -> None:
        self.spin = spin

    def dance(self, programs):
        return programs[len(programs) - self.spin:] + programs[:len(programs) - self.spin]


class Exchange(Move):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def dance(self, programs):
        programs[self.x], programs[self.y] = programs[self.y], programs[self.x] 
        return programs


class Partner(Move):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def dance(self, programs):
        x, y = programs.index(self.x), programs.index(self.y)
        programs[x], programs[y] = programs[y], programs[x] 
        return programs


def parse_input():
    def parse_move(line):
        if line[0] == "s":
            return Spin(int(line[1:]))
        elif line[0] == "x":
            return Exchange(*[int(x) for x in line[1:].split("/")])
        elif line[0] == "p":
            return Partner(*[ord(x) - ord("a") for x in line[1:].split("/")])
        raise ValueError(f"Cant parse {line}")

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_move(inst) for inst in f.readline().strip().split(",")]


def to_alpha(programs):
    return "".join([chr(ord("a") + x) for x in programs])


def main():
    moves = parse_input()
    programs = list(range(16))
    seen = {}
    i = 0
    while to_alpha(programs) not in seen:
        seen[to_alpha(programs)] = i
        i += 1
        for move in moves:
            programs = move.dance(programs)
        if i % 1000 == 0:
            logger.info(f"loop {i}")
    seen_rev = {step: node for node, step in seen.items()}
    logger.info(f"Res A {seen_rev[1]}")
    pos = 1000000000
    logger.info(f"Res B {seen_rev[pos % i]}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
