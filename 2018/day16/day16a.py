from collections import namedtuple

class Opcode:
    def __init__(self, action):
        self._action = action

    def execute(self, registers, a, b, c):
        new_reg = list(registers)
        new_reg[c] = self.calculate_val(new_reg, a, b)
        return new_reg

    def calculate_val(self, registers, a, b):
        pass


class ROpcode(Opcode):
    def calculate_val(self, registers, a, b):
        return self._action(registers[a], registers[b])

class IOpcode(Opcode):
    def calculate_val(self, registers, a, b):
        return self._action(registers[a], b)

class IROpcode(Opcode):
    def calculate_val(self, registers, a, b):
        return self._action(a, registers[b])


addr = ROpcode(lambda a, b: a+b)
addi = IOpcode(lambda a, b: a+b)
mulr = ROpcode(lambda a, b: a*b)
muli = IOpcode(lambda a, b: a*b)
banr = ROpcode(lambda a, b: a&b)
bani = IOpcode(lambda a, b: a&b)
borr = ROpcode(lambda a, b: a|b)
bori = IOpcode(lambda a, b: a|b)
setr = ROpcode(lambda a, b: a)
seti = IROpcode(lambda a, b: a)
gtir = IROpcode(lambda a, b: 1 if a > b else 0)
gtri = IOpcode(lambda a, b: 1 if a > b else 0)
gtrr = ROpcode(lambda a, b: 1 if a > b else 0)
eqir = IROpcode(lambda a, b: 1 if a == b else 0)
eqri = IOpcode(lambda a, b: 1 if a == b else 0)
eqrr = ROpcode(lambda a, b: 1 if a == b else 0)

Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])
Sample = namedtuple('Sample', ['instruction', 'before_reg', 'after_reg'])

def parse_registers(reg_str):
    return [int(x) for x in reg_str[1:-1].split(', ')]


def read_input():
    samples = []
    program = []

    with open('input.txt') as f:
        is_sample = False
        before_reg = None
        instruction = None
        for line in f:
            if not line.strip():
                pass
            elif line.startswith('Before: '):
                is_sample = True
                before_reg = parse_registers(line[len('Before: '):].strip())
                pass
            elif line.startswith('After: '):
                after_reg = parse_registers(line[len('After: '):].strip())
                samples.append(Sample(instruction, before_reg, after_reg))
                before_reg = None
                instruction = None
                is_sample = False
            elif is_sample:
                instruction = Instruction(*[int(x) for x in line.split(' ')])
            else:
                program.append(Instruction(*[int(x) for x in line.split(' ')]))
    return samples, program


def test_op_code(op, sample):
    res = op.execute(sample.before_reg, sample.instruction.a, sample.instruction.b, sample.instruction.c)
    return res == sample.after_reg


def get_matched(matching_dict):
    for k, v in matching_dict.items():
        if len(v) == 1:
            return k, v.pop()
    return None, None


def decode_opcodes(samples, operations):
    matching_codes = {i: set(operations) for i in range(len(operations))}
    for sample in samples:
        #print('Before sample %d' % len(matching_codes[sample.instruction.opcode]))
        for op in operations:
            if not test_op_code(op, sample):
                matching_codes[sample.instruction.opcode].discard(op)
        #print('After sample %d' % len(matching_codes[sample.instruction.opcode]))
    matched = {}
    opcode_num, opcode = get_matched(matching_codes)
    while opcode_num is not None:
        matched[opcode_num] = opcode
        for v in matching_codes.values():
            v.discard(opcode)
        opcode_num, opcode = get_matched(matching_codes)

    return matched


def execute_program(program, decoded_opcodes):
    registers = [0, 0, 0, 0]
    for instruction in program:
        opcode = decoded_opcodes[instruction.opcode]
        registers = opcode.execute(registers, instruction.a, instruction.b, instruction.c)
    return registers

def main():
    operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr,
                  seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    samples, program = read_input()
    print(len(samples))

    #test_output = [[test_op_code(op, sample)for op in operations] for sample in samples]
    #print(sum([sum(outputs) >= 3 for outputs in test_output]))
    decoded_opcodes = decode_opcodes(samples, operations)
    print(decoded_opcodes)

    registers = execute_program(program, decoded_opcodes)
    print(registers)

if __name__ == '__main__':
    main()
