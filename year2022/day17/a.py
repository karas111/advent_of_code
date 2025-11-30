import logging
import os
from typing import NamedTuple

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

ROCKS = [
    [Cords(i, 0) for i in range(4)],
    [Cords(1, 0), Cords(0, 1), Cords(1, 1), Cords(2, 1), Cords(1, 2)],
    [Cords(0, 0), Cords(1, 0), Cords(2, 0), Cords(2, 1), Cords(2, 2)],
    [Cords(0, i) for i in range(4)],
    [Cords(0, 0), Cords(1, 0), Cords(0, 1), Cords(1, 1)],
]
JET_MOVE = {"<": Cords(-1, 0), ">": Cords(1, 0)}
WIDTH = 7


class RockState(NamedTuple):
    left_edge: int
    rock_idx: int
    jets_idx: int
    relative_col_heights: tuple


def read_jets() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def simulate(jets: str, steps: int, stop_on_cycle: bool = False) -> int:
    visited = {Cords(i, 0) for i in range(WIDTH)}

    def move(rock: list[Cords], dc: Cords) -> tuple[bool, list[Cords]]:
        new_rock = [r_c + dc for r_c in rock]
        if any(r_c in visited for r_c in new_rock):
            return False, rock
        return True, new_rock

    col_max_heights = [0] * WIDTH
    states = {}
    step_n, rock_idx, jets_idx = 0, 0, 0
    while step_n < steps:
        max_height = max(col_max_heights)
        # add walls, the top edge of rock is 7 unit heigher than max_height at most
        for i in range(max_height + 1, max_height + 8):
            visited.add(Cords(-1, i))
            visited.add(Cords(WIDTH, i))
        start_cord = Cords(2, max_height + 4)
        rock = [c + start_cord for c in ROCKS[rock_idx]]

        moved = True
        while moved:
            jet_move = JET_MOVE[jets[jets_idx]]
            _, rock = move(rock, jet_move)
            moved, rock = move(rock, Cords(0, -1))
            jets_idx = (jets_idx + 1) % len(jets)

        for r_c in rock:
            visited.add(r_c)
            col_max_heights[r_c.x] = max(col_max_heights[r_c.x], r_c.y)

        rock_idx = (rock_idx + 1) % len(ROCKS)

        max_rock_y = max(r_c.y for r_c in rock)
        state = RockState(
            left_edge=min(r_c.x for r_c in rock),
            rock_idx=rock_idx,
            jets_idx=jets_idx,
            relative_col_heights=tuple(y - max_rock_y for y in col_max_heights),
        )
        if state in states:
            max_h = max(col_max_heights)
            cycle_prev_step, cycle_max_h = states[state]
            cycle_len = step_n - cycle_prev_step
            logger.info("Found cycle at idx %d, len %d.", step_n, cycle_len)
            cycle_dh = max(col_max_heights) - cycle_max_h
            left = steps - 1 - step_n
            n_cycles = left // cycle_len
            offset = left % cycle_len
            offset_h = [
                h for step, h in states.values() if step == cycle_prev_step + offset
            ][0]
            offset_dh = offset_h - cycle_max_h
            max_h = max_h + offset_dh + n_cycles * cycle_dh
            return max_h
        else:
            states[state] = (step_n, max(col_max_heights))

        step_n += 1

    return max(col_max_heights)


def main():
    jets = read_jets()
    res = simulate(jets, 2022)
    logger.info("Result a %d", res)
    res = simulate(jets, 1000000000000)
    logger.info("Result b %d", res)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
