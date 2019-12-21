import copy
import logging
import os
from asyncio import Queue, gather

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine

logger = logging.getLogger(__name__)


async def put_instruction(instruction: str, computer):
    for i in instruction:
        await computer.input.put(ord(i))
    await computer.input.put(ord('\n'))


async def program_droid(computer: Computer):
    insts = [
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'AND D J'
    ]
    for inst in insts:
        await put_instruction(inst, computer)
    await put_instruction('WALK', computer)


async def program_droid_run(computer: Computer):
    insts = [
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'AND D J',

        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J'
    ]
    for inst in insts:
        await put_instruction(inst, computer)
    await put_instruction('RUN', computer)


def get_comp_output(computer):
    res = []
    for c in computer.flush_output():
        if c < 0x110000:
            res.append(chr(c))
        else:
            res.append(str(c))
    return ''.join(res)


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(
        os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    await gather(computer.execute(), program_droid(computer))
    logger.info('Result a:\n%s', get_comp_output(computer))

    computer = Computer(copy.copy(program), Queue(), Queue())
    await gather(computer.execute(), program_droid_run(computer))
    logger.info('Result a:\n%s', get_comp_output(computer))


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
