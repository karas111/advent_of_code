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
        return parse_input({"out": OutInst}, f)


class OutInst(Instruction):
    def execute(self, registers, pointer):
        logger.info("Out: %d", self._get_value(self.a, registers))
        return pointer + 1


def main():
    instructions = m_parse()
    a = 1
    pointer = 0
    registers = {"a": a, "b": 0, "c": 0, "d": 0}
    while False and pointer >= 0 and pointer < len(instructions):
        inst = instructions[pointer]
        pointer = inst.execute_with_insts(registers, pointer, instructions)
    # the program translates to
    a_start = 1
    while False:
        a = 14*182 + a_start
        while a:
            b = a%2
            a = a//2
            logger.info(b)

    # For blinking endles signal
    # the binary represetnation of a + 14*182 needs to be
    # 1010101010....
    # so we are looking for first such number greater than 14*182
    start_n = 14*182
    len_num = len(bin(start_n)[2:])
    expected = 0
    signal = True
    for _ in range(len_num):
        expected = expected << 1
        expected += signal
        signal = not signal
    logger.info(expected)
    logger.info(bin(expected))
    logger.info("Res a %s", expected-start_n)



if __name__ == "__main__":
    init_logging()
    main()
