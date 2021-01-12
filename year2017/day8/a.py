import logging
import re
import os
import time
from collections import namedtuple
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Instruction = namedtuple(
    "Instruction", ["reg_out", "inc", "by", "reg_in", "op", "comp"]
)

OPS = {
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
}


def parse_input():
    def parse_instrunction(line):
        match = re.match(r"(\w+) (inc|dec) (.+) if (\w+) (.+) (.+)", line)
        reg_out, inc, by, reg_in, op, comp = match.groups()
        return Instruction(reg_out, inc == "inc", int(by), reg_in, op, int(comp))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_instrunction(line.strip()) for line in f.readlines() if line]


def execute_instructions(instructions: List[Instruction]):
    res = {}
    total_max = 0
    for inst in instructions:
        if OPS[inst.op](res.setdefault(inst.reg_in, 0), inst.comp):
            n_val = res.get(inst.reg_out, 0) + inst.by * (inst.inc and 1 or -1)
            res[inst.reg_out] = n_val
            total_max = max(total_max, n_val)
    return res, total_max


def main():
    instructions = parse_input()
    res, total_max = execute_instructions(instructions)
    logger.info(f"Res A {max(res.values())}")
    logger.info(f"Res B {total_max}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
