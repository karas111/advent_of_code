import copy
import logging
import os
from asyncio import Queue, create_task, sleep
from collections import deque

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine

logger = logging.getLogger(__name__)


class ComputerState:
    def __init__(self, computer: Computer):
        self.computer = computer
        self.buffer = deque()


async def generate_computers(program, n=50):
    res = []
    for i in range(n):
        computer = Computer(copy.copy(program), Queue(), Queue())
        await computer.input.put(i)
        res.append(ComputerState(computer))
    return res


async def supervisor(computer_states, with_nat_handlig=False):
    logger.info('In supervisor')
    tasks = [create_task(c.computer.execute()) for c in computer_states]
    logger.info('Computers started')
    nat_pos = None
    last_send_nat_y = None
    while True:
        # Read phase
        for idx, state in enumerate(computer_states):
            computer = state.computer
            # logger.info('Reading from %d', idx)
            if not computer.output.empty():
                address = await computer.output.get()
                x = await computer.output.get()
                y = await computer.output.get()
                # logger.info('Received from %d, to %d, (%d, %d)', idx, address, x, y)
                if address == 255:
                    if with_nat_handlig:
                        nat_pos = (x, y)
                    else:
                        for task in tasks:
                            task.cancel()
                        return y
                else:
                    computer_states[address].buffer.append(x)
                    computer_states[address].buffer.append(y)
        # Write phase
        blocked = 0
        for idx, state in enumerate(computer_states):
            if len(state.buffer):
                while len(state.buffer):
                    await state.computer.input.put(state.buffer.popleft())
            else:
                blocked += 1
                await state.computer.input.put(-1)
        if blocked == len(computer_states) and with_nat_handlig and nat_pos is not None:
            await computer_states[0].computer.input.put(nat_pos[0])
            await computer_states[0].computer.input.put(nat_pos[1])
            if last_send_nat_y == nat_pos[1]:
                for task in tasks:
                    task.cancel()
                return last_send_nat_y
            else:
                last_send_nat_y = nat_pos[1]
        await sleep(0)


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(
        os.path.dirname(__file__), "input.txt"))
    computer_states = await generate_computers(program)
    res = await supervisor(computer_states)
    logger.info('Result a:%s', res)
    computer_states = await generate_computers(program)
    res = await supervisor(computer_states, with_nat_handlig=True)
    logger.info('Result b:%s', res)


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
