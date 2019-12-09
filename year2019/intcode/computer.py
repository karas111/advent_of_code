from enum import Enum
import logging

logger = logging.getLogger(__name__)


class OpCode:

    def __init__(self, idx, computer):
        self.idx = idx
        self.op_code = computer.program[idx]
        self.computer = computer
        self.exit = False

    @staticmethod
    def create(computer, idx):
        op_code = computer.program.get(idx, Computer.UNITIALIZED_MEM) % 100
        if op_code == 99:
            return ExitOp(idx, computer)
        elif op_code == 1:
            return AddOp(idx, computer)
        elif op_code == 2:
            return MultOp(idx, computer)
        elif op_code == 3:
            return InputOp(idx, computer)
        elif op_code == 4:
            return OutputOp(idx, computer)
        elif op_code == 5:
            return JumpTrueOp(idx, computer)
        elif op_code == 6:
            return JumpFalseOp(idx, computer)
        elif op_code == 7:
            return LessOp(idx, computer)
        elif op_code == 8:
            return EqualsOp(idx, computer)
        elif op_code == 9:
            return RelativeBaseOp(idx, computer)
        else:
            raise ValueError('No such opcode %d' % op_code)

    def read_raw_arg(self, arg_n, positional_ind):
        program = self.computer.program
        result = program.get(self.idx + 1 + arg_n, Computer.UNITIALIZED_MEM)
        if positional_ind == 2:
            result += self.computer.relative_base
        return result

    def get_arg(self, arg_n, write=False):
        program = self.computer.program
        positional_ind = (self.op_code // 10 ** (2 + arg_n)) % 10
        arg_raw = self.read_raw_arg(arg_n, positional_ind)
        if positional_ind in {0, 2}:
            if write:
                return arg_raw
            else:
                return program.get(arg_raw, Computer.UNITIALIZED_MEM)
        elif positional_ind == 1:
            return arg_raw
        else:
            raise ValueError()


class TwoArgResultOpCode(OpCode):

    def exec_func(self, args0, args1):
        raise NotImplementedError()

    def execute_program(self, input, output):
        program = self.computer.program
        args0 = self.get_arg(0)
        args1 = self.get_arg(1)
        program[self.get_arg(2, write=True)] = self.exec_func(args0, args1)
        return self.idx + 4, ComputerState.RUNNING


class ExitOp(OpCode):

    def __init__(self, idx, computer):
        super().__init__(idx, computer)
        self.exit = True

    def execute_program(self, input, output):
        return self.idx + 1, ComputerState.FINISHED


class AddOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 + args1


class MultOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 * args1


class InputOp(OpCode):

    def execute_program(self, input, output):
        program = self.computer.program
        if len(input) == 0:
            return self.idx, ComputerState.PAUSED
        program[self.get_arg(0, write=True)] = input.pop(0)
        return self.idx + 2, ComputerState.RUNNING


class OutputOp(OpCode):

    def execute_program(self, input, output):
        args0 = self.get_arg(0)
        output.append(args0)
        return self.idx + 2, ComputerState.RUNNING


class JumpSinlgeArgOpCode(OpCode):

    def compare_arg(self, args0):
        raise NotImplementedError()

    def execute_program(self, input, output):
        args0 = self.get_arg(0)
        if self.compare_arg(args0):
            return self.get_arg(1), ComputerState.RUNNING
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


class RelativeBaseOp(OpCode):

    def execute_program(self, input, output):
        args0 = self.get_arg(0)
        self.computer.relative_base += args0
        return self.idx + 2, ComputerState.RUNNING


class ComputerState(Enum):
    PAUSED = 1
    RUNNING = 2
    FINISHED = 3


class Computer:
    UNITIALIZED_MEM = 0

    def __init__(self, program, input, output, idx=0, relative_base=0):
        self.program = dict(enumerate(program))
        self.input = input
        self.output = output
        self.idx = idx
        self.relative_base = relative_base
        self.state = ComputerState.PAUSED

    def execute(self):
        if self.state != ComputerState.PAUSED:
            raise ValueError('Can not run computer in state %s' % self.state)
        self.state = ComputerState.RUNNING
        while True:
            op_code = OpCode.create(self, self.idx)
            self.idx, self.state = op_code.execute_program(self.input, self.output)
            if self.state in [ComputerState.PAUSED, ComputerState.FINISHED]:
                return
