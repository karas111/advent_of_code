import os


def read_program():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
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
        else:
            raise ValueError()

    def get_arg(self, arg_n, program):
        positional_ind = (self.op_code // 10 ** (2 + arg_n)) % 10
        arg_raw = program[self.idx + 1 + arg_n]
        if positional_ind == 0:
            return program[arg_raw]
        elif positional_ind == 1:
            return arg_raw
        else:
            raise ValueError()


class ExitOp(OpCode):

    def __init__(self, idx, program):
        super().__init__(idx, program)
        self.exit = True

    def execute_program(self, program, input, output):
        return self.idx + 1


class AddOp(OpCode):

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        args1 = self.get_arg(1, program)
        program[program[self.idx + 3]] = args0 + args1
        return self.idx + 4


class MultOp(OpCode):

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        args1 = self.get_arg(1, program)
        program[program[self.idx + 3]] = args0 * args1
        return self.idx + 4


class InputOp(OpCode):

    def execute_program(self, program, input, output):
        program[program[self.idx + 1]] = input.pop(0)
        return self.idx + 2


class OutputOp(OpCode):

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        output.append(args0)
        return self.idx + 2


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
    # program = [1002, 4, 3, 4, 33]
    input = [1]
    output = execute_program(program, input)
    print(output)
    print(program)


if __name__ == "__main__":
    main()
