import logging
import os

from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Inst = tuple[str, int]

CORDS_MAP = {"U": Cords(0, -1), "D": Cords(0, 1), "L": Cords(-1, 0), "R": Cords(1, 0)}


def read_inst() -> list[Inst]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            direction, step = line.strip().split()
            res.append((direction, int(step)))
    return res


def do_instruction(insts: list[Inst], knots_n: int = 2) -> set[Cords]:
    res = set()
    knots = [Cords(0, 0) for _ in range(knots_n)]
    res.add(knots[-1])
    for inst in insts:
        direction = CORDS_MAP[inst[0]]
        for _ in range(inst[1]):
            knots[0] = knots[0] + direction
            for i in range(1, knots_n):
                h_cords = knots[i - 1]
                t_cords = knots[i]
                diff_cords = h_cords - t_cords
                if abs(diff_cords.x) < 2 and abs(diff_cords.y) < 2:
                    continue
                dx, dy = 0, 0
                if diff_cords.x < 0:
                    dx = -1
                elif diff_cords.x > 0:
                    dx = 1
                if diff_cords.y < 0:
                    dy = -1
                elif diff_cords.y > 0:
                    dy = 1
                t_cords += Cords(dx, dy)
                knots[i] = t_cords
                if i == knots_n - 1:
                    res.add(t_cords)
    return res


def main():
    insts = read_inst()
    res = do_instruction(insts)
    logger.info("Result a %s", len(res))
    res = do_instruction(insts, 10)
    logger.info("Result b %s", len(res))


if __name__ == "__main__":
    init_logging()
    main()
