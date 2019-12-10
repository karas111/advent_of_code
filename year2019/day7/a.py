import asyncio
import copy
import logging
import os
from itertools import permutations

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import run_main_coroutine

AMPLIFIER_NUM = 5


def generate_circut_a(program, sequence_num):
    input_output = []
    for i in sequence_num:
        input_output.append(asyncio.Queue())
        input_output[-1].put_nowait(i)

    input_output.append(asyncio.Queue())
    input_output[0].put_nowait(0)
    return[Computer(copy.copy(program), input_output[i], input_output[i+1]) for i in range(AMPLIFIER_NUM)]


def generate_circut_b(program, sequence_num):
    input_output = []
    for i in sequence_num:
        input_output.append(asyncio.Queue())
        input_output[-1].put_nowait(i)
    input_output[0].put_nowait(0)
    return[Computer(copy.copy(program), input_output[i], input_output[(i+1) % AMPLIFIER_NUM]) for i in range(AMPLIFIER_NUM)]


async def run_simulation(computers):
    await asyncio.gather(*[computer.execute() for computer in computers])
    return computers


async def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    simulations = [
        (generate_circut_a, permutations(range(AMPLIFIER_NUM))),
        (generate_circut_b, permutations(range(AMPLIFIER_NUM, AMPLIFIER_NUM*2)))
    ]
    for circuit_generator, sequences in simulations:
        last_outputs = []
        for sequence_num in sequences:
            computers = circuit_generator(program, sequence_num)
            await run_simulation(computers)
            last_outputs.append(computers[-1].flush_output()[-1])
            # logging.warning('Finished for simulation %s. Output is %d', sequence_num, computers[-1].output[-1])
        logging.warning('Max signal %d', max(last_outputs))


if __name__ == "__main__":
    run_main_coroutine(main)
