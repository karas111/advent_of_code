import copy
from itertools import permutations
import os

from year2019.day5.a import execute_program, read_program

AMPLIFIER_NUM = 5


def run_simulation1(programs, sequence_num):
    outputs = []
    output = None
    for i in range(AMPLIFIER_NUM):
        program = programs[i]
        input = [sequence_num[i]]
        if output is not None:
            input += output
        else:
            input.append(0)
        output = execute_program(program, input)
        outputs.append(output)
    return outputs


def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    sequences = permutations(range(AMPLIFIER_NUM))
    last_outputs = []
    programs = [copy.copy(program) for i in range(AMPLIFIER_NUM)]
    for sequence_num in sequences:
        outputs = run_simulation1(programs, sequence_num)
        last_outputs.append(outputs[-1][-1])
        # print(outputs)
    print('Max signal %d' % max(last_outputs))


if __name__ == "__main__":
    main()
