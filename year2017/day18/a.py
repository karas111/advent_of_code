import logging
from collections import namedtuple
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


State = namedtuple("State", ["registers", "pointer", "last_sound", "exit"])


class Program:
    def __init__(self, instructions, prog_id) -> None:
        self.instructions = instructions
        self.rcv_queue = []
        self.snd_queue = None
        self.locked = False
        self.snd_counter = 0
        self.state = State({"p": prog_id}, pointer=0, last_sound=None, exit=False)

    def execute(self):
        while True:
            inst = self.instructions[self.state.pointer]
            self.state = inst.execute(self.state, self)
            if self.locked:
                return


class Instruction:
    def __init__(self, a) -> None:
        self.a = a

    def execute(self, state_in: State, program: Program = None) -> State:
        raise NotImplementedError()

    def _get_value(self, arg, registers):
        if isinstance(arg, str):
            return registers.get(arg, 0)
        return arg


class TwoArgsInstruction(Instruction):
    def __init__(self, a, b) -> None:
        super().__init__(a)
        self.b = b

    def get_value_b(self, registers):
        return self._get_value(self.b, registers)

    def operation(self, x: int, y: int) -> int:
        raise NotImplementedError()

    def execute(self, state_in: State, program: Program = None) -> State:
        state_in.registers[self.a] = self.operation(state_in.registers.get(self.a, 0), self.get_value_b(state_in.registers))
        return state_in._replace(pointer=state_in.pointer + 1, exit=False)


class AddInst(TwoArgsInstruction):
    def operation(self, x: int, y: int) -> int:
        return x + y


class MultInst(TwoArgsInstruction):
    def operation(self, x: int, y: int) -> int:
        return x * y


class ModInst(TwoArgsInstruction):
    def operation(self, x: int, y: int) -> int:
        return x % y


class SetInst(TwoArgsInstruction):
    def operation(self, x: int, y: int) -> int:
        return y


class JmpInst(TwoArgsInstruction):
    def execute(self, state_in: State, program: Program = None) -> State:
        a_val = self._get_value(self.a, state_in.registers)
        pointer_d = a_val > 0 and self.get_value_b(state_in.registers) or 1
        return state_in._replace(pointer=state_in.pointer + pointer_d, exit=False)


class SndInst(Instruction):
    def execute(self, state_in: State, program: Program = None) -> State:
        if program is not None:
            program.snd_queue.append(self._get_value(self.a, state_in.registers))
            program.snd_counter += 1
            return state_in._replace(pointer=state_in.pointer + 1)
        else:
            return state_in._replace(pointer=state_in.pointer + 1, exit=False, last_sound=self._get_value(self.a, state_in.registers))


class RcvInst(Instruction):
    def execute(self, state_in: State, program: Program = None) -> State:

        if program is not None:
            if program.rcv_queue:
                program.locked = False
                state_in.registers[self.a] = program.rcv_queue.pop(0)
                return state_in._replace(pointer=state_in.pointer + 1)
            else:
                program.locked = True
                return state_in._replace(pointer=state_in.pointer)
        else:
            a_val = self._get_value(self.a, state_in.registers)
            exit = a_val != 0
            return state_in._replace(pointer=state_in.pointer + 1, exit=exit)


def parse_input():
    INST_MAP = {
        "add": AddInst,
        "mul": MultInst,
        "mod": ModInst,
        "set": SetInst,
        "jgz": JmpInst,
        "snd": SndInst,
        "rcv": RcvInst,
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


def main():
    instructions = parse_input()
    state_in = State(registers={}, pointer=0, last_sound=None, exit=False)
    while not state_in.exit:
        inst = instructions[state_in.pointer]
        state_in = inst.execute(state_in)
    logger.info(f"Res A {state_in.last_sound}")

    progs = [Program(instructions, prog_id=0),  Program(instructions, prog_id=1)]
    progs[0].snd_queue, progs[1].snd_queue = progs[1].rcv_queue, progs[0].rcv_queue
    last_snd_counter = (None, None)
    while True:
        new_snd_counters = (progs[0].snd_counter, progs[1].snd_counter)
        if last_snd_counter == new_snd_counters and progs[0].locked and progs[1].locked:
            logger.info(f"Res B {progs[1].snd_counter}")
            break
        last_snd_counter = new_snd_counters
        for i in range(2):
            progs[i].execute()


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
