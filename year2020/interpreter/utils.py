from typing import List

from year2020.interpreter.computer import Acc, Instruction, Jmp, NoOp


def parse_line(line: str) -> Instruction:
    op, arg = line.split(" ")
    arg = int(arg)
    if op == "nop":
        return NoOp(arg)
    elif op == "acc":
        return Acc(arg)
    elif op == "jmp":
        return Jmp(arg)
    else:
        raise ValueError(f"Can't parse {line}")


def read_program(path: str) -> List[Instruction]:
    with open(path) as f:
        program = [parse_line(line.strip()) for line in f if line]
    return program
