import logging
import os
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_instructions() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.read()


def find_insts(inst: str) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    insts = [(int(a), int(b)) for a, b in pattern.findall(inst)]
    return insts


def calculate(insts: list[tuple[int, int]]) -> int:
    return sum(a * b for a, b in insts)


def find_insts2(insts: str) -> int:
    pattern = re.compile(r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))")
    do = True
    res = []
    for inst, a, b in pattern.findall(insts):
        if inst == "do()":
            do = True
        elif inst == "don't()":
            do = False
        else:
            if do:
                res.append((int(a), int(b)))
    return res


def main():
    instructions = read_instructions()
    insts = find_insts(instructions)

    logger.info("Result a %s", calculate(insts))
    insts = find_insts2(instructions)
    logger.info("Result b %s", calculate(insts))


if __name__ == "__main__":
    init_logging()
    main()
