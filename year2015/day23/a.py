import logging
import os
from abc import abstractmethod
from dataclasses import dataclass

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


@dataclass
class State:
    instr: int
    registers: dict[str, int]


class Instruction:
    def __init__(self, register: str):
        self.register = register

    @abstractmethod
    def execute(self, state: State) -> None: ...


class Hlf(Instruction):
    def execute(self, state):
        state.instr += 1
        state.registers[self.register] //= 2


class Tpl(Instruction):
    def execute(self, state):
        state.instr += 1
        state.registers[self.register] *= 3


class Inc(Instruction):
    def execute(self, state):
        state.instr += 1
        state.registers[self.register] += 1


class Jmp(Instruction):
    def __init__(self, offset):
        super().__init__(None)
        self.offset = offset

    def execute(self, state):
        state.instr += self.offset


class Jie(Instruction):
    def __init__(self, register, offset):
        super().__init__(register)
        self.offset = offset

    def execute(self, state):
        if state.registers[self.register] % 2 == 0:
            state.instr += self.offset
        else:
            state.instr += 1


class Jio(Instruction):
    def __init__(self, register, offset):
        super().__init__(register)
        self.offset = offset

    def execute(self, state):
        if state.registers[self.register] == 1:
            state.instr += self.offset
        else:
            state.instr += 1


def read_input() -> list[Instruction]:
    res = []

    def parse_inst(line: str) -> Instruction:
        params = line[4:].split(", ")
        match line[:3]:
            case "hlf":
                return Hlf(params[0])
            case "tpl":
                return Tpl(params[0])
            case "inc":
                return Inc(params[0])
            case "jmp":
                return Jmp(int(params[0]))
            case "jie":
                return Jie(params[0], int(params[1]))
            case "jio":
                return Jio(params[0], int(params[1]))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        while True:
            line = f.readline().strip()
            if not line:
                return res
            res.append(parse_inst(line))


def simulate(insts: list[Instruction], part_b: bool) -> int:
    state = State(0, {"a": 1 if part_b else 0, "b": 0})
    while state.instr < len(insts):
        inst = insts[state.instr]
        inst.execute(state)
    return state.registers["b"]


def main():
    insts = read_input()
    res = simulate(insts, part_b=False)
    logger.info("Res a: %s", res)
    res = simulate(insts, part_b=True)
    logger.info("Res b: %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
