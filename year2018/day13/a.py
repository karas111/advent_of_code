import logging
import os
import time
from collections import namedtuple
from enum import Enum

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Point = namedtuple("Point", ["pos", "velocity"])


class Direction(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


DIRECTIONS_ORD = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

MOVE_VEC = {
    Direction.NORTH: np.array([0, -1]),
    Direction.EAST: np.array([1, 0]),
    Direction.SOUTH: np.array([0, 1]),
    Direction.WEST: np.array([-1, 0]),
}


class Cart:
    def __init__(self, pos, dir) -> None:
        super().__init__()
        self.pos = pos
        self.dir = dir
        self.next_turn = 0  # 0 for left, 1 for straight, 2 for right

    def __repr__(self) -> str:
        return f"Cart({self.pos[0]}, {self.pos[1]}), {self.dir.value}"

    def step(self, grid):
        self.pos += MOVE_VEC[self.dir]
        x, y = self.pos
        symb = grid[y][x]
        if (symb == "|" and self.dir in [Direction.NORTH, Direction.SOUTH]) or (
            symb == "-" and self.dir in [Direction.EAST, Direction.WEST]
        ):
            pass
        elif symb == "+":
            dir_id = DIRECTIONS_ORD.index(self.dir)
            self.dir = DIRECTIONS_ORD[(dir_id + self.next_turn - 1) % 4]
            self.next_turn = (self.next_turn + 1) % 3
        elif symb in "/\\":
            turn = -1 if self.dir in [Direction.EAST, Direction.WEST] else 1
            turn *= -1 if symb == "\\" else 1
            dir_id = DIRECTIONS_ORD.index(self.dir)
            self.dir = DIRECTIONS_ORD[(dir_id + turn) % 4]
        else:
            raise ValueError(
                f"wrong combination of symbol and direction {symb}, {self.dir}"
            )


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        grid = [[c for c in line.strip("\n")] for line in f.readlines() if line]
    carts = []
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c in "<>v^":
                carts.append(Cart(np.array([x, y]), Direction(c)))
                grid[y][x] = c in "<>" and "-" or "|"
    return carts, grid


def simulate(carts, grid):
    posns = set(tuple(c.pos) for c in carts)
    while True:
        carts = sorted(carts, key=lambda c: (c.pos[1], c.pos[0]))

        for cart in carts:
            posns.remove(tuple(cart.pos))
            cart.step(grid)
            new_pos = tuple(cart.pos)
            if new_pos in posns:
                return new_pos
            posns.add(new_pos)


def simulate_b(carts, grid):
    posns = set(tuple(c.pos) for c in carts)
    while True:
        carts = sorted(carts, key=lambda c: (c.pos[1], c.pos[0]))
        if len(carts) <= 1:
            return tuple(carts[0].pos)

        carts_to_remove = set()
        for cart in carts:
            if cart in carts_to_remove:
                continue

            posns.remove(tuple(cart.pos))
            cart.step(grid)
            new_pos = tuple(cart.pos)
            if new_pos in posns:
                crashed = {cart for cart in carts if tuple(cart.pos) == new_pos}
                assert len(crashed) <= 2
                carts_to_remove = carts_to_remove | crashed
                posns.remove(new_pos)
            else:
                posns.add(new_pos)
        carts = [cart for cart in carts if cart not in carts_to_remove]


def main():
    carts, grid = parse_input()
    crash = simulate(carts, grid)
    logger.info(f"First crash {crash}")
    carts, grid = parse_input()
    crash = simulate_b(carts, grid)
    logger.info(f"Last cart {crash}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
