import copy
import logging
import os
from typing import List

from year2019.utils import init_logging
from year2020.interpreter.computer import Computer, Instruction, Jmp, NoOp
from year2020.interpreter.utils import read_program

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class InspectableComputer(Computer):
    def __init__(self, program: List[Instruction], accumulator: int = 0, idx: int = 0):
        super().__init__(program, accumulator=accumulator, idx=idx)
        self.visited_inst = set()
        self.abnormal_end = False

    def check_stop(self):
        if self.idx in self.visited_inst:
            self.abnormal_end = True
            return True
        return super().check_stop()

    def run_one_step(self):
        self.visited_inst.add(self.idx)
        return super().run_one_step()


def find_failing_inst(program):
    for i in range(len(program)):
        inst = program[i]
        new_program = copy.copy(program)
        if isinstance(inst, NoOp):
            new_program[i] = Jmp(inst.arg)
        elif isinstance(inst, Jmp):
            new_program[i] = NoOp(inst.arg)
        else:
            continue
        computer = InspectableComputer(new_program)
        computer.run()
        if not computer.abnormal_end:
            logger.info(f"Found failed instruction = {i}")
            return computer
    raise ValueError("Not found instruction")


def main():
    program = read_program(os.path.join(os.path.dirname(__file__), INPUT_FILE))
    computer = InspectableComputer(program)
    computer.run()
    logger.info(f"Acc {computer.accumulator}, idx {computer.idx}")
    computer = find_failing_inst(program)
    logger.info(f"Acc {computer.accumulator}, idx {computer.idx}")


if __name__ == "__main__":
    init_logging()
    main()
