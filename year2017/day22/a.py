import logging
import os
import time
from enum import Enum

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class CellState(Enum):
    INFECTED = 1
    WEAKEND = 2
    FLAGGED = 3
    CLEAN = 4


CELL_TRANSITIONS = {
    CellState.INFECTED: CellState.FLAGGED,
    CellState.FLAGGED: CellState.CLEAN,
    CellState.CLEAN: CellState.WEAKEND,
    CellState.WEAKEND: CellState.INFECTED,
}

CELL_TURNS = {
    CellState.INFECTED: 1,
    CellState.FLAGGED: 2,
    CellState.CLEAN: -1,
    CellState.WEAKEND: 0,
}


class Carrier:
    def __init__(self, cords, direction) -> None:
        self.cords = cords
        self.direction = direction


MOVE_VEC = [
    (0, -1),  # NORTH
    (1, 0),  # EAST
    (0, 1),  # SOUTH
    (-1, 0),  # WEST
]


def parse_input():
    infected = set()
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        grid = [line.strip() for line in f.readlines() if line]
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                if c == "#":
                    infected.add((x, y))
    return infected, (len(grid[0]) // 2, len(grid) // 2)


def burst_a(infected, carrier):
    turn = carrier.cords in infected and 1 or -1
    carrier.direction = (carrier.direction + turn) % len(MOVE_VEC)
    res = carrier.cords not in infected
    if carrier.cords in infected:
        infected.remove(carrier.cords)
    else:
        infected.add(carrier.cords)
    dx, dy = MOVE_VEC[carrier.direction]
    carrier.cords = (carrier.cords[0] + dx, carrier.cords[1] + dy)
    return res


def burst_b(infected, carrier):
    cell_state = infected.get(carrier.cords, CellState.CLEAN)
    turn = CELL_TURNS[cell_state]
    carrier.direction = (carrier.direction + turn) % len(MOVE_VEC)
    new_state = CELL_TRANSITIONS[cell_state]
    res = new_state == CellState.INFECTED
    infected[carrier.cords] = new_state
    dx, dy = MOVE_VEC[carrier.direction]
    carrier.cords = (carrier.cords[0] + dx, carrier.cords[1] + dy)
    return res


def do_bursts(infected, carrier, n_bursts, part_b=False):
    res = 0
    for _ in range(n_bursts):
        if part_b:
            res += burst_b(infected, carrier)
        else:
            res += burst_a(infected, carrier)
    return res


def main():
    infected, cords = parse_input()
    carrier = Carrier(cords, 0)
    res_a = do_bursts(infected, carrier, 10000)
    logger.info(f"Res A {res_a}")
    infected, cords = parse_input()
    carrier = Carrier(cords, 0)
    infected = {coord: CellState.INFECTED for coord in infected}
    res_b = do_bursts(infected, carrier, 10000000, part_b=True)
    logger.info(f"Res B {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
