from enum import Enum
import logging

logger = logging.getLogger(__name__)


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
        return self.idx + 4, ComputerState.RUNNING


class ExitOp(OpCode):

    def __init__(self, idx, program):
        super().__init__(idx, program)
        self.exit = True

    def execute_program(self, program, input, output):
        return self.idx + 1, ComputerState.FINISHED


class AddOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 + args1


class MultOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 * args1


class InputOp(OpCode):

    def execute_program(self, program, input, output):
        if len(input) == 0:
            return self.idx, ComputerState.PAUSED
        program[program[self.idx + 1]] = input.pop(0)
        return self.idx + 2, ComputerState.RUNNING


class OutputOp(OpCode):

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        output.append(args0)
        return self.idx + 2, ComputerState.RUNNING


class JumpSinlgeArgOpCode(OpCode):

    def compare_arg(self, args0):
        raise NotImplementedError()

    def execute_program(self, program, input, output):
        args0 = self.get_arg(0, program)
        if self.compare_arg(args0):
            return self.get_arg(1, program), ComputerState.RUNNING
        else:
            return self.idx + 3, ComputerState.RUNNING


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


class ComputerState(Enum):
    PAUSED = 1
    RUNNING = 2
    FINISHED = 3


class Computer:

    def __init__(self, program, input, output, idx=0):
        self.program = program
        self.input = input
        self.output = output
        self.idx = idx
        self.state = ComputerState.PAUSED

    def execute(self):
        if self.state != ComputerState.PAUSED:
            raise ValueError('Can not run computer in state %s' % self.state)
        self.state = ComputerState.RUNNING
        while True:
            op_code = OpCode.create(self.program, self.idx)
            self.idx, self.state = op_code.execute_program(
                self.program, self.input, self.output)
            if self.state in [ComputerState.PAUSED, ComputerState.FINISHED]:
                return
