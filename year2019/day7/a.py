import copy
import logging
import os
from itertools import permutations

from year2019.intcode.computer import Computer, ComputerState
from year2019.intcode.utils import read_program

AMPLIFIER_NUM = 5


def generate_circut_a(program, sequence_num):
    input_output = [[i] for i in sequence_num]
    input_output.append([])
    input_output[0].append(0)
    return[Computer(copy.copy(program), input_output[i], input_output[i+1]) for i in range(AMPLIFIER_NUM)]


def generate_circut_b(program, sequence_num):
    input_output = [[i] for i in sequence_num]
    input_output[0].append(0)
    return[Computer(copy.copy(program), input_output[i], input_output[(i+1) % AMPLIFIER_NUM]) for i in range(AMPLIFIER_NUM)]


def run_simulation(computers):
    while any(computer.state != ComputerState.FINISHED for computer in computers):
        for comp_id, computer in enumerate(computers):
            computer.execute()
    return computers


def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    simulations = [
        (generate_circut_a, permutations(range(AMPLIFIER_NUM))),
        (generate_circut_b, permutations(range(AMPLIFIER_NUM, AMPLIFIER_NUM*2)))
    ]
    for circuit_generator, sequences in simulations:
        last_outputs = []
        for sequence_num in sequences:
            computers = circuit_generator(program, sequence_num)
            run_simulation(computers)
            last_outputs.append(computers[-1].output[-1])
            # logging.warning('Finished for simulation %s. Output is %d', sequence_num, computers[-1].output[-1])
        logging.warning('Max signal %d', max(last_outputs))


if __name__ == "__main__":
    main()
