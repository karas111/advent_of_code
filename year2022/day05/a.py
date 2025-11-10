import logging
import os
import re
from collections import namedtuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Instruction = namedtuple("Instruction", "n from_ to")


def read_input() -> tuple[list[list[str]], list[Instruction]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = []
        for line in f:
            line = line.strip("\n")
            if not line:
                break
            lines.append(line)
        n_stacks = int(lines[-1][-2])
        stacks = [[] for _ in range(n_stacks)]
        for line in reversed(lines[:-1]):
            for i in range(n_stacks):
                c = line[1 + 4 * i]
                if c != " ":
                    stacks[i].append(c)
        pattern = r"^move (\d+) from (\d+) to (\d+)$"
        insts = [
            Instruction(*map(int, line))
            for line in re.findall(pattern, f.read(), re.MULTILINE)
        ]
        return stacks, insts


def move(stacks: list[list[str]], insts: list[Instruction], reverse_mode: bool):
    for inst in insts:
        to_move = stacks[inst.from_ - 1][-inst.n :]
        if reverse_mode:
            to_move.reverse()
        stacks[inst.from_ - 1] = stacks[inst.from_ - 1][: -inst.n]
        stacks[inst.to - 1].extend(to_move)


def main():
    stacks, insts = read_input()
    move(stacks, insts, True)
    logger.info("Result a %s", "".join(stack[-1] for stack in stacks))
    stacks, insts = read_input()
    move(stacks, insts, False)
    logger.info("Result b %s", "".join(stack[-1] for stack in stacks))


if __name__ == "__main__":
    init_logging()
    main()
