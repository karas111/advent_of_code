from enum import Enum
import logging

logger = logging.getLogger(__name__)


class OpCode:

    def __init__(self, computer):
        self.computer = computer

    @staticmethod
    def create(computer):
        op_code_mapper = {
            99: ExitOp,
            1: AddOp,
            2: MultOp,
            3: InputOp,
            4: OutputOp,
            5: JumpTrueOp,
            6: JumpFalseOp,
            7: LessOp,
            8: EqualsOp,
            9: RelativeBaseOp
        }
        op_code = computer.program.get(computer.idx, Computer.UNITIALIZED_MEM) % 100
        op_code_generator = op_code_mapper.get(op_code)
        if op_code_generator is None:
            raise ValueError('No such opcode %d' % op_code)
        return op_code_generator(computer)


class TwoArgResultOpCode(OpCode):

    def exec_func(self, args0, args1):
        raise NotImplementedError()

    def execute_program(self):
        args0 = self.computer.read_mem(0)
        args1 = self.computer.read_mem(1)
        self.computer.write_mem(2, self.exec_func(args0, args1))
        self.computer.increase_inst(4)
        return ComputerState.RUNNING


class ExitOp(OpCode):

    def execute_program(self):
        self.computer.increase_inst(1)
        return ComputerState.FINISHED


class AddOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 + args1


class MultOp(TwoArgResultOpCode):

    def exec_func(self, args0, args1):
        return args0 * args1


class InputOp(OpCode):

    def execute_program(self):
        if len(self.computer.input) == 0:
            return ComputerState.PAUSED
        self.computer.write_mem(0, self.computer.input.pop(0))
        self.computer.increase_inst(2)
        return ComputerState.RUNNING


class OutputOp(OpCode):

    def execute_program(self):
        args0 = self.computer.read_mem(0)
        self.computer.output.append(args0)
        self.computer.increase_inst(2)
        return ComputerState.RUNNING


class JumpSinlgeArgOpCode(OpCode):

    def compare_arg(self, args0):
        raise NotImplementedError()

    def execute_program(self):
        args0 = self.computer.read_mem(0)
        if self.compare_arg(args0):
            self.computer.set_inst(self.computer.read_mem(1))
            return ComputerState.RUNNING
        else:
            self.computer.increase_inst(3)
            return ComputerState.RUNNING


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

    def execute_program(self):
        args0 = self.computer.read_mem(0)
        self.computer.increase_releative_base(args0)
        self.computer.increase_inst(2)
        return ComputerState.RUNNING


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

    def _read_raw_arg(self, arg_n):
        op_code = self.program[self.idx]
        positional_ind = (op_code // 10 ** (2 + arg_n)) % 10
        result = self.program.get(self.idx + 1 + arg_n, Computer.UNITIALIZED_MEM)
        if positional_ind == 2:
            result += self.relative_base
        return result, positional_ind

    def read_mem(self, arg_n):
        arg_raw, positional_ind = self._read_raw_arg(arg_n)
        if positional_ind in {0, 2}:
            return self.program.get(arg_raw, Computer.UNITIALIZED_MEM)
        elif positional_ind == 1:
            return arg_raw

    def write_mem(self, arg_n, value):
        arg_raw, positional_ind = self._read_raw_arg(arg_n)
        if positional_ind in {0, 2}:
            self.program[arg_raw] = value
        elif positional_ind == 1:
            return ValueError('Can not write to instant argument')
        else:
            raise ValueError()

    def increase_releative_base(self, inc):
        self.relative_base += inc

    def increase_inst(self, inc):
        self.idx += inc

    def set_inst(self, idx):
        self.idx = idx

    def execute(self):
        if self.state != ComputerState.PAUSED:
            raise ValueError('Can not run computer in state %s' % self.state)
        self.state = ComputerState.RUNNING
        while True:
            op_code = OpCode.create(self)
            self.state = op_code.execute_program()
            if self.state in [ComputerState.PAUSED, ComputerState.FINISHED]:
                return
