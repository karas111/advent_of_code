import logging
import os
from typing import List, NamedTuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

VECTORS = {"forward": (1, 0), "up": (0, -1), "down": (0, 1)}


class Instruction(NamedTuple):
    inst: str
    number: int


def read_inst():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            if line:
                inst, number = line.split(" ")
                yield Instruction(inst, int(number))


def find_pos(instructions: List[Instruction]):
    pos = (0, 0)
    for inst in instructions:
        vec = VECTORS[inst.inst]
        pos = pos[0] + vec[0] * inst.number, pos[1] + vec[1] * inst.number
    return pos


def find_pos_aim(instructions: List[Instruction]):
    pos = (0, 0)
    aim = 0
    for inst in instructions:
        if inst.inst in ["up", "down"]:
            aim += inst.number * (inst.inst == "up" and -1 or 1)
        else:
            pos = pos[0] + inst.number, pos[1] + inst.number * aim
    return pos


def main():
    instructions = list(read_inst())
    res = find_pos(instructions)
    logger.info(f"Result a {res}, {res[0] * res[1]}")
    res = find_pos_aim(instructions)
    logger.info(f"Result a {res}, {res[0] * res[1]}")


if __name__ == "__main__":
    init_logging()
    main()
