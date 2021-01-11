import logging
import os
import time
from collections import namedtuple
from typing import List

import numpy as np

from year2019.utils import init_logging
from z3 import If, Int, Optimize

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Nanobot = namedtuple("Nanobot", ["pos", "r"])


def find_largest(nanobots: List[Nanobot]) -> Nanobot:
    return max(*nanobots, key=lambda n: n.r)


def parse_input():
    def parse_bot(line) -> Nanobot:
        cords, r = line.split(">, r=")
        cords = np.array([int(x) for x in cords[len("pos=<") :].split(",")])
        r = int(r)
        return Nanobot(cords, r)

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_bot(line.strip()) for line in f.readlines() if line]


def distance(n: Nanobot, other: Nanobot) -> int:
    return sum(np.absolute(n.pos - other.pos))


def z3_abs(x):
    return If(x < 0, -x, x)


def z3_dist(cords, bot_pos):
    return (
        z3_abs(bot_pos[0] - cords[0])
        + z3_abs(bot_pos[1] - cords[1])
        + z3_abs(bot_pos[2] - cords[2])
    )


def part_b(nanobots):
    x = Int("x")
    y = Int("y")
    z = Int("z")
    cords = (x, y, z)
    cost_expr = x * 0
    for bot in nanobots:
        cost_expr += If(z3_dist(cords, bot.pos) <= bot.r, 1, 0)
    cost = Int("cost")
    opt = Optimize()
    opt.add(cost == cost_expr)
    opt.maximize(cost)
    opt.minimize(z3_dist(cords, (0, 0, 0)))
    opt.check()
    model = opt.model()
    res = model[x].as_long(), model[y].as_long(), model[z].as_long()
    return res


def main():
    nanobots = parse_input()
    max_nano = find_largest(nanobots)
    distances = [distance(max_nano, n) for n in nanobots]
    in_range = [d for d in distances if d <= max_nano.r]
    logger.info(f"Res A {len(in_range)}")
    pos = part_b(nanobots)
    logger.info(f"Res B is {pos}, {sum(np.absolute(np.array(pos)))}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
