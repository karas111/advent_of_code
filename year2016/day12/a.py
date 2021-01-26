import functools
import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Instruction:
    def __init__(self, a) -> None:
        self.a = a

    def execute(self, registers, pointer) -> int:
        raise NotImplementedError()

    def _get_value(self, arg, registers):
        if isinstance(arg, str):
            return registers.get(arg, 0)
        return arg


class TwoArgsInstruction(Instruction):
    def __init__(self, a, b) -> None:
        super().__init__(a)
        self.b = b


class IncInst(Instruction):
    def execute(self, registers, pointer) -> int:
        registers[self.a] += 1
        return pointer + 1


class DecInst(Instruction):
    def execute(self, registers, pointer) -> int:
        registers[self.a] -= 1
        return pointer + 1


class CpyInst(TwoArgsInstruction):
    def execute(self, registers, pointer) -> int:
        registers[self.b] = self._get_value(self.a, registers)
        return pointer + 1


class JnzInst(TwoArgsInstruction):
    def execute(self, registers, pointer) -> int:
        if self._get_value(self.a, registers) != 0:
            return pointer + self._get_value(self.b, registers)
        else:
            return pointer + 1


def parse_input():
    INST_MAP = {
        "cpy": CpyInst,
        "inc": IncInst,
        "dec": DecInst,
        "jnz": JnzInst,
    }

    def parse_arg(arg):
        try:
            return int(arg)
        except Exception:
            return arg

    def parse_inst(line):
        inst, *args = line.split(" ")
        return INST_MAP[inst](*[parse_arg(arg) for arg in args])

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_inst(line.strip()) for line in f.readlines() if line]


@functools.lru_cache(None)
def fib(n):
    if n in (-1, 0):
        return 1
    return fib(n - 2) + fib(n - 1)


def main():
    instructions = parse_input()
    pointer = 0
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    while False and pointer >= 0 and pointer < len(instructions):
        inst = instructions[pointer]
        pointer = inst.execute(registers, pointer)
    d = 26
    logger.info(f"Res A {fib(d) + 16*17}")
    d = 33
    logger.info(f"Res B {fib(d) + 16*17}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
