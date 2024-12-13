import logging
import os
import re
from dataclasses import dataclass
from typing import Optional

from catch_time import catchtime
from year2019.utils import init_logging
from z3 import Ints, Solver, sat

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


@dataclass
class Game:
    a: tuple[int, int]
    b: tuple[int, int]
    prize: tuple[int, int]


def read_input() -> list[Game]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        idx = 0
        lines = f.readlines()
        button_pattern = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
        prize_pattern = re.compile(r"Prize: X=(\d+), Y=(\d+)")
        while idx < len(lines):
            a = tuple(map(int, re.match(button_pattern, lines[idx]).groups()))
            b = tuple(map(int, re.match(button_pattern, lines[idx + 1]).groups()))
            prize = tuple(map(int, re.match(prize_pattern, lines[idx + 2]).groups()))
            idx += 4
            yield Game(a, b, prize)


def solve_m(g: Game) -> Optional[int]:
    b0 = g.prize[0] * g.a[1] - g.prize[1] * g.a[0]
    b1 = g.b[0] * g.a[1] - g.b[1] * g.a[0]
    if b0 % b1 != 0:
        return 0
    b = b0 // b1
    a0 = g.prize[0] - b * g.b[0]
    if a0 % g.a[0] != 0:
        return 0
    a = a0 // g.a[0]
    return int(a) * 3 + int(b)


def solve_z3(g: Game) -> Optional[int]:
    a, b = Ints("a b")
    s = Solver()
    s.add(a >= 0)
    s.add(b >= 0)
    s.add(a*g.a[0] + b*g.b[0] == g.prize[0])
    s.add(a*g.a[1] + b*g.b[1] == g.prize[1])
    if s.check() != sat:
        return 0
    m = s.model()
    return m[a].as_long() * 3 + m[b].as_long()


def main():
    games = list(read_input())
    with catchtime(logger):
        logger.info("Res A %s", sum(solve_z3(game) for game in games))
        for g in games:
            g.prize = tuple(x + 10000000000000 for x in g.prize)
        logger.info("Res B %s", sum(solve_z3(game) for game in games))

    games = list(read_input())
    with catchtime(logger):
        logger.info("Res A %s", sum(solve_m(game) for game in games))
        for g in games:
            g.prize = tuple(x + 10000000000000 for x in g.prize)
        logger.info("Res B %s", sum(solve_m(game) for game in games))


if __name__ == "__main__":
    init_logging()
    main()
