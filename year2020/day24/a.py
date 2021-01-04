import itertools
import logging
import os
import time
from collections import deque
from typing import Deque, Tuple, List, Dict
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

DIRECTIONS = {
    "e": (0, 1),
    "w": (0, -1),
    "ne": (-1, 1),
    "nw": (-1, 0),
    "se": (1, 0),
    "sw": (1, -1),
}

def read_input() -> List[List[str]]:
    def parse_line(line: str) -> List[str]:
        idx = 0
        res = []
        while idx < len(line):
            if line[idx] in "ns":
                res.append(line[idx:idx+2])
                idx += 2
            else:
                res.append(line[idx:idx+1])
                idx += 1
        return res

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_line(line.strip()) for line in f.readlines() if line]


def run_instruction(insts: List[str]):
    pos = (0, 0)
    directions = [DIRECTIONS[inst] for inst in insts]
    y, x = zip(*directions)
    return sum(y), sum(x)


def flip(insts: List[List[str]]):
    grid = set()
    for inst in insts:
        cords = run_instruction(inst)
        if cords in grid:
            grid.remove(cords)
        else:
            grid.add(cords)
    return grid


def play_life(grid, n_rounds=100):
    for i in range(n_rounds):
        new_grid = set()
        to_check = set()
        for tile in grid:
            to_check.add(tile)
            for dy, dx in DIRECTIONS.values():
                to_check.add((tile[0] + dy, tile[1] + dx))
        for cords in to_check:
            blacks = sum((cords[0] + dy, cords[1]+ dx) in grid for dy, dx in DIRECTIONS.values())
            if cords in grid and 0 < blacks < 3:
                new_grid.add(cords)
            elif cords not in grid and blacks == 2:
                new_grid.add(cords)
        grid = new_grid
        logger.info(f"Round {i}, blacks {len(grid)}")


def main():
    instructions = read_input()
    grid = flip(instructions)
    logger.info(f"Res A {len(grid)}")
    play_life(grid, n_rounds=100)


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
