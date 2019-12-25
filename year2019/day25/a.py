import copy
import logging
import os
from asyncio import Queue, create_task, sleep
from collections import deque

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program
from year2019.utils import init_logging, run_main_coroutine

logger = logging.getLogger(__name__)


class GameInterface:
    CMD_MAP = {
        'N': 'north',
        'S': 'south',
        'E': 'east',
        'W': 'west',
        'I': 'inv'
    }

    AVOID_ITEMS = [
        'escape pod',
        'molten lava',
        'photons'
    ]

    def __init__(self, computer: Computer, initial_commands: list):
        self.computer = computer
        self.all_commands = []
        self.initial_commands = initial_commands

    async def run(self):
        for com in self.initial_commands:
            await self.send_command(com)
        task = create_task(self.computer.execute())
        while not self.computer.finished:
            await self.print_computer_output()
            await self.pass_manual_command()
        task.cancel()

    async def print_computer_output(self):
        buffer = []
        while True:
            await sleep(0)
            buffer += [chr(c) for c in self.computer.flush_output()]
            buffer_str = ''.join(buffer)
            if buffer_str.endswith('Command?\n') or self.computer.finished:
                logger.info(buffer_str)
                return

    async def pass_manual_command(self):
        manual_cmd = input('--> ')
        cmd = self.CMD_MAP.get(manual_cmd, manual_cmd)
        if cmd == 'history':
            logger.info('Commands history:\n%s', ', '.join(self.all_commands))
            await self.pass_manual_command()
        else:
            await self.send_command(cmd)

    async def send_command(self, cmd):
        logger.info('Sending command: %s', cmd)
        for c in cmd:
            await self.computer.input.put(ord(c))
        await self.computer.input.put(ord('\n'))
        self.all_commands.append(cmd)


async def main():
    logger.info('Start...')
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    computer = Computer(copy.copy(program), Queue(), Queue())
    INITIAL_COMMANDS = [
        'north',
        'take wreath',
        'east',
        'east',
        'west',
        'west',
        'north',
        'east'

    ]
    gi = GameInterface(computer, initial_commands=INITIAL_COMMANDS)
    await gi.run()


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
