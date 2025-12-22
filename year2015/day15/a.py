import logging
import math
import os
import re
from typing import NamedTuple

from z3 import If, Int, Optimize

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Ingreedient(NamedTuple):
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def read_input() -> list[Ingreedient]:
    pattern = r"\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            args = re.match(pattern, line.strip()).groups()
            res.append(Ingreedient(*map(int, args)))
    return res


def optimize_qty(ingredients: list[Ingreedient], part_b: bool = False) -> int:
    ingr_qty = []
    requiremenets = []
    for idx in range(len(ingredients)):
        qty = Int(f"qty_{idx}")
        requiremenets.append(qty >= 0)
        ingr_qty.append(qty)
    requiremenets.append(sum(ingr_qty) == 100)

    total_factors = []
    for field in Ingreedient._fields:
        factor = sum(qty * getattr(i, field) for qty, i in zip(ingr_qty, ingredients))
        if field != "calories":
            factor = If(factor < 0, 0, factor)
            total_factors.append(factor)
        elif part_b:
            requiremenets.append(factor == 500)

    total_score = math.prod(total_factors)

    opt = Optimize()
    opt.add(*requiremenets)
    opt.maximize(total_score)
    opt.check()
    model = opt.model()
    res = model.eval(total_score).as_long()
    return res


def main():
    ingreedients = read_input()
    logger.info("Res a: %d", optimize_qty(ingreedients))
    logger.info("Res b: %d", optimize_qty(ingreedients, part_b=True))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
