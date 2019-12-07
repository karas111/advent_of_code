import os


def read_program(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(path) as f:
        program = [int(n) for n in f.readline().split(",")]
    return program


class OpCode:

    def __init__(self, idx, program):
        self.idx = idx
        self.op_code = program[idx]
        self.exit = False

    @staticmethod
    def create(program, idx):
        op_code = program[idx] % 100
        if op_code == 99:
            return ExitOp(idx, program)
        elif op_code == 1:
            return AddOp(idx, program)
        elif op_code == 2:
            return MultOp(idx, program)
        elif op_code == 3:
            return InputOp(idx, program)
        elif op_code == 4:
            return OutputOp(idx, program)
        elif op_code == 5:
            return JumpTrueOp(idx, program)
        elif op_code == 6:
            return JumpFalseOp(idx, program)
        elif op_code == 7:
            return LessOp(idx, program)
        elif op_code == 8:
            return EqualsOp(idx, program)
        else:
            raise ValueError('No such opcode %d' % op_code)

    def get_arg(self, arg_n, program):
        positional_ind = (self.op_code // 10 ** (2 + arg_n)) % 10
        arg_raw = program[self.idx + 1 + arg_n]
        if positional_ind == 0:
            return program[arg_raw]
        elif positional_ind == 1:
            return arg_raw
        else:
            raise ValueError()


class TwoArgResultOpCode(OpCode):

    def exec_func(self, args0, args1):
        raise NotImplementedError()

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        args1 = self.get_arg(1, program)
        program[program[self.idx + 3]] = self.exec_func(args0, args1)
        return self.idx + 4


class ExitOp(OpCode):

    def __init__(self, idx, program):
        super().__init__(idx, program)
        self.exit = True

    def execute_program(self, program, input, output):
        return self.idx + 1


class AddOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 + args1


class MultOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 * args1


class InputOp(OpCode):

    def execute_program(self, program, input, output):
        program[program[self.idx + 1]] = input.pop(0)
        return self.idx + 2


class OutputOp(OpCode):

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        output.append(args0)
        return self.idx + 2


class JumpSinlgeArgOpCode(OpCode):

    def compare_arg(self, args0):
        raise NotImplementedError()

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        if self.compare_arg(args0):
            return self.get_arg(1, program)
        else:
            return self.idx + 3


class JumpTrueOp(JumpSinlgeArgOpCode):

    def compare_arg(self, args0):
        return args0 != 0


class JumpFalseOp(JumpSinlgeArgOpCode):

    def compare_arg(self, args0):
        return args0 == 0


class LessOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return int(args0 < args1)


class EqualsOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return int(args0 == args1)


def execute_program(program, input, output=None, idx=0):
    if output is None:
        output = []
    while True:
        op_code = OpCode.create(program, idx)
        idx = op_code.execute_program(program, input, output)
        if op_code.exit:
            return output


def main():
    program = read_program()
    # program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #            1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #            999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    input = [1]
    output = execute_program(program, input)
    print(output)
    print(program)


if __name__ == "__main__":
    main()
