import logging
import os
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum
from functools import cache

from catch_time import catchtime
from year2019.utils import init_logging
from z3 import BitVec, Optimize

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class OperandType(Enum):
    LITERAL = "literal"
    COMBO = "combo"


class Instruction(ABC):
    OPERAND_TYPE = OperandType.LITERAL
    _OP_CODE_TO_REGISTER = {
        4: "A",
        5: "B",
        6: "C",
    }

    def __init__(self, operand: int):
        self._op = operand

    def resolve_operand(self, cmp: "Computer") -> int:
        if self.OPERAND_TYPE == OperandType.LITERAL:
            return self._op
        # COMBO operand
        if 0 <= self._op <= 3:
            return self._op
        if self._op == 7:
            raise ValueError("Invalid operand")
        return cmp.get_register(self._OP_CODE_TO_REGISTER[self._op])

    @abstractmethod
    def _run(self, cmp: "Computer") -> None: ...

    def _modify_pointer(self, cmp: "Computer") -> None:
        cmp.inc_pointer()

    def run_with_pointer(self, cmp: "Computer") -> None:
        self._run(cmp)
        self._modify_pointer(cmp)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._op})"


class Dv(Instruction):
    OPERAND_TYPE = OperandType.COMBO
    _WRITE_REG = None

    def _run(self, cmp: "Computer") -> None:
        numerator = cmp.get_register("A")
        denominator = 2 ** self.resolve_operand(cmp)
        cmp.set_register(self._WRITE_REG, numerator // denominator)


class Adv(Dv):
    _WRITE_REG = "A"


class Bdv(Dv):
    _WRITE_REG = "B"


class Cdv(Dv):
    _WRITE_REG = "C"


class Bxl(Instruction):
    OPERAND_TYPE = OperandType.LITERAL

    def _run(self, cmp: "Computer") -> None:
        val = cmp.get_register("B") ^ self.resolve_operand(cmp)
        cmp.set_register("B", val)


class Bst(Instruction):
    OPERAND_TYPE = OperandType.COMBO

    def _run(self, cmp: "Computer") -> None:
        val = self.resolve_operand(cmp) % 8
        cmp.set_register("B", val)


class Jnz(Instruction):
    OPERAND_TYPE = OperandType.LITERAL

    def _run(self, cmp: "Computer") -> None: ...

    def _modify_pointer(self, cmp: "Computer") -> None:
        val = cmp.get_register("A")
        if val == 0:
            cmp.inc_pointer()
        else:
            cmp.set_pointer(self.resolve_operand(cmp))


class Bxc(Instruction):
    OPERAND_TYPE = OperandType.LITERAL

    def _run(self, cmp: "Computer") -> None:
        val = cmp.get_register("B") ^ cmp.get_register("C")
        cmp.set_register("B", val)


class Out(Instruction):
    OPERAND_TYPE = OperandType.COMBO

    def _run(self, cmp: "Computer") -> None:
        val = self.resolve_operand(cmp) % 8
        cmp.output(val)


OP_TO_INST_MAP = [Adv, Bxl, Bst, Jnz, Bxc, Out, Bdv, Cdv]


class Computer:

    def __init__(self, registers: dict[str, int], instructions: list[int]):
        self._pointer = 0
        self._registers = registers
        self._instructions = instructions
        self._output = []

    def get_register(self, reg: str) -> int:
        return self._registers[reg]

    def set_register(self, reg: str, value: int) -> None:
        self._registers[reg] = value

    def set_pointer(self, pointer: int) -> None:
        self._pointer = pointer

    def inc_pointer(self) -> None:
        self._pointer += 2

    def output(self, val: int) -> None:
        self._output.append(val)

    def print_output(self) -> str:
        return ",".join(map(str, self._output))

    @cache
    def generate_instruction(self, op_code: int, operand: int) -> Instruction:
        return OP_TO_INST_MAP[op_code](operand)

    def run(self):
        while self._pointer < len(self._instructions):
            opcode, operand = self._instructions[self._pointer : self._pointer + 2]
            inst = self.generate_instruction(opcode, operand)
            # logger.info("%s %s\n%s", self._pointer, self._registers, inst)
            inst.run_with_pointer(self)
            # logger.info("%s", self._registers)


def read_input() -> Computer:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(r"\d+")
        a = int(re.search(pattern, f.readline()).group(0))
        b = int(re.search(pattern, f.readline()).group(0))
        c = int(re.search(pattern, f.readline()).group(0))
        f.readline()
        instructions = list(map(int, re.findall(pattern, f.readline())))
    return Computer({"A": a, "B": b, "C": c}, instructions)


def program(a: int, break_on_first: bool = True) -> list[int]:
    b = 0
    c = 0
    res = []
    while True:
        b = a % 8  # bst(4)
        b = b ^ 5  # bxl(5)
        c = a >> b  # cdv(5)
        a = a >> 3  # adv(3)
        b = b ^ c  # bxc(0)
        b = b ^ 6  # bxl(6)
        res.append(b % 8)  # out(5)
        if break_on_first:
            return res
        if a == 0:
            break
    return res


def part2(expected_outs: list[int]) -> int:
    # only 10 bits matters in term of the first output of the program
    mapped_outs = defaultdict(list)
    for a in range(2**10):
        mapped_outs[program(a)[0]].append(a)
    possible_a = set(mapped_outs[expected_outs[0]])
    for depth in range(1, len(expected_outs)):
        expected_out = expected_outs[depth]
        new_possible_a = set()
        depth_possible_a = mapped_outs[expected_out]
        for a in possible_a:
            moved_a = a >> (3 * depth)
            remainder = a & ((1 << (3 * depth)) - 1)
            for depth_a in depth_possible_a:
                first_7_bits = depth_a & ((1 << 7) - 1)
                if first_7_bits == moved_a:
                    new_possible_a.add((depth_a << (3 * depth)) + remainder)

        possible_a = new_possible_a
        depth += 1
    return min(possible_a)

def part2_z3(insts = list[int]) -> int:
    opt = Optimize()
    s = BitVec("s", 64)
    a, b, c = s, 0, 0
    for x in insts:
        b = a % 8
        b = b ^ 5
        c = a / (1 << b)
        a = a / (1 << 3)
        b = b ^ c
        b = b ^ 6
        opt.add((b % 8) == x)
    opt.add(a == 0)
    opt.minimize(s)
    assert str(opt.check()) == 'sat'
    return opt.model().eval(s)

def main():
    cmp = read_input()
    with catchtime(logger):
        cmp.run()
        logger.info("Res A %s", cmp.print_output())

        b = part2(cmp._instructions)
        logger.info("Res B: %s", b)
        logger.info("%s", program(b, break_on_first=False))


if __name__ == "__main__":
    init_logging()
    main()
