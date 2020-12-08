from typing import List


class Instruction:
    def __init__(self, arg: int) -> None:
        super().__init__()
        self.arg = arg

    def run(self, computer):
        raise NotImplementedError("Must be implemented in subclass")


class NoOp(Instruction):

    def run(self, computer: 'Computer'):
        computer.idx += 1


class Acc(Instruction):

    def run(self, computer):
        computer.accumulator += self.arg
        computer.idx += 1


class Jmp(Instruction):

    def run(self, computer):
        computer.idx += self.arg


class Computer:
    UNITIALIZED_MEM = 0

    def __init__(self, program: List[Instruction], accumulator: int = 0, idx: int = 0):
        self.program = program
        self.accumulator = accumulator
        self.idx = idx

    def run_one_step(self):
        inst = self.program[self.idx]
        return inst.run(self)

    def check_stop(self):
        return self.idx >= len(self.program)

    def run(self):
        while not self.check_stop():
            self.run_one_step()
