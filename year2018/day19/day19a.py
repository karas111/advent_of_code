from collections import namedtuple
import os
import logging


INPUT_FILE = "input.txt"


class Opcode:
    def __init__(self, action):
        self._action = action

    def execute(self, registers, a, b, c):
        try:
            new_reg = list(registers)
            new_reg[c] = self.calculate_val(new_reg, a, b)
        except Exception:
            print([k for k, v in OPCODES.items() if v == self])
            print("err")
            raise
        return new_reg

    def calculate_val(self, registers, a, b):
        pass


class ROpcode(Opcode):
    def calculate_val(self, registers, a, b):
        try:
            b_val = registers[b]
        except Exception:
            b_val = None
        return self._action(registers[a], b_val)


class IOpcode(Opcode):
    def calculate_val(self, registers, a, b):
        return self._action(registers[a], b)


class IROpcode(Opcode):
    def calculate_val(self, registers, a, b):
        try:
            b_val = registers[b]
        except:
            b_val = None
        return self._action(a, b_val)


addr = ROpcode(lambda a, b: a + b)
addi = IOpcode(lambda a, b: a + b)
mulr = ROpcode(lambda a, b: a * b)
muli = IOpcode(lambda a, b: a * b)
banr = ROpcode(lambda a, b: a & b)
bani = IOpcode(lambda a, b: a & b)
borr = ROpcode(lambda a, b: a | b)
bori = IOpcode(lambda a, b: a | b)
setr = ROpcode(lambda a, b: a)
seti = IROpcode(lambda a, b: a)
gtir = IROpcode(lambda a, b: 1 if a > b else 0)
gtri = IOpcode(lambda a, b: 1 if a > b else 0)
gtrr = ROpcode(lambda a, b: 1 if a > b else 0)
eqir = IROpcode(lambda a, b: 1 if a == b else 0)
eqri = IOpcode(lambda a, b: 1 if a == b else 0)
eqrr = ROpcode(lambda a, b: 1 if a == b else 0)

OPCODES = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}

Instruction = namedtuple("Instruction", ["opcode", "a", "b", "c"])


def read_input(filename=None):
    instruction_pointer = None
    program = []
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), INPUT_FILE)
    with open(filename) as f:
        for line in f:
            if line.startswith("#ip"):
                instruction_pointer = int(line[len("#ip") :].strip())
            else:
                opcode_str, a, b, c = line.split(" ")
                program.append(Instruction(OPCODES[opcode_str], int(a), int(b), int(c)))

    return program, instruction_pointer


def execute_program(program, ip, registers=None, max_iter=10 ** 15):
    if registers is None:
        registers = [1, 0, 0, 0, 0, 0]

    while registers[ip] < len(program) and max_iter:
        max_iter -= 1
        instruction = program[registers[ip]]
        registers = instruction.opcode.execute(
            registers, instruction.a, instruction.b, instruction.c
        )
        registers[ip] += 1
        logging.info(f"Registers {registers}")
    return registers


def main():
    program, ip = read_input()
    print(program)
    print(ip)
    # registers = execute_program(program, ip)
    # print(registers)

    n = 10551326
    sum = 0
    for i in range(1, n + 1):
        if n % i == 0:
            sum += i
    print(sum)


if __name__ == "__main__":
    main()
