import logging
from multiprocessing import Value
import os
from math import factorial

from year2016.day12.a import (CpyInst, DecInst, IncInst, Instruction, JnzInst,
                              TwoArgsInstruction, parse_input)
from year2019.utils import init_logging

INPUT_FILE = "input.txt"

logger = logging.getLogger(__name__)


def m_parse():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return parse_input({"tgl": TglInst}, f)


class TglInst(Instruction):
    def execute(self, registers, pointer):
        raise ValueError("Use execute_with_insts")

    def execute_with_insts(self, registers, pointer, insts) -> int:
        to_toggle_idx = pointer + self._get_value(self.a, registers)
        if to_toggle_idx >= len(insts):
            return pointer + 1
        current_inst = insts[to_toggle_idx]
        new_inst = None
        if isinstance(current_inst, IncInst):
            new_inst = DecInst(current_inst.a)
        elif isinstance(current_inst, JnzInst):
            new_inst = CpyInst(current_inst.a, current_inst.b)
        elif isinstance(current_inst, TwoArgsInstruction):
            new_inst = JnzInst(current_inst.a, current_inst.b)
        else:
            new_inst = IncInst(current_inst.a)
        insts[to_toggle_idx] = new_inst
        return pointer + 1


def main():
    instructions = m_parse()
    pointer = 0
    registers = {"a": 7, "b": 0, "c": 0, "d": 0}
    while False and pointer >= 0 and pointer < len(instructions):
        inst = instructions[pointer]
        pointer = inst.execute_with_insts(registers, pointer, instructions)
    logger.info("Reg %s", registers)
    logger.info("Res %s", factorial(7) + 87 * 77)
    logger.info("Res %s", factorial(12) + 87 * 77)


if __name__ == "__main__":
    init_logging()
    main()
