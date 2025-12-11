import logging
import os
from typing import NamedTuple

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVES = {
    ">": Cords(1, 0),
    "<": Cords(-1, 0),
    "^": Cords(0, -1),
    "v": Cords(0, 1),
}


class Blizzard(NamedTuple):
    cords: Cords
    step: str
    width: str
    height: str

    def move(self) -> "Blizzard":
        n_cords = self.cords + MOVES[self.step]
        return Blizzard(
            Cords(n_cords.x % self.width, n_cords.y % self.height),
            self.step,
            self.width,
            self.height,
        )


def read_input() -> list[Blizzard]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.readlines()
        h = len(lines) - 2
        for y, line in enumerate(lines):
            line = line.strip()
            w = len(line) - 2
            for x, c in enumerate(line):
                if c not in "<^>v":
                    continue
                cords = Cords(
                    x - 1,
                    y - 1,
                )
                res.append(Blizzard(cords, c, w, h))
        return res


def simulate(blizzards: list[Blizzard], start: Cords, end: Cords) -> int:
    w, h = blizzards[0].width, blizzards[0].height
    positions = {start}
    step = 0
    while True:
        step += 1
        blizzards = [b.move() for b in blizzards]
        occupied = {b.cords for b in blizzards}
        new_possisions = set()
        for current_pos in positions:
            to_check = [current_pos + dc for dc in MOVES.values()]
            to_check.append(current_pos)
            for n_pos in to_check:
                if n_pos in occupied:
                    continue
                if (
                    (n_pos.x < 0 or n_pos.x >= w or n_pos.y < 0 or n_pos.y >= h)
                    and n_pos != start
                    and n_pos != end
                ):
                    continue
                new_possisions.add(n_pos)
        positions = new_possisions
        if end in new_possisions:
            return step, blizzards
    return -1, []


def main():
    blizzards = read_input()
    start = Cords(0, -1)
    end = Cords(blizzards[0].width - 1, blizzards[0].height)
    res_a, blizzards = simulate(blizzards, start, end)
    logger.info("Result a %s", res_a)
    res_b1, blizzards = simulate(blizzards, end, start)
    res_b2, blizzards = simulate(blizzards, start, end)
    logger.info("Result a %s", res_a + res_b1 + res_b2)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
