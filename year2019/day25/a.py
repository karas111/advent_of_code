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

    ALL_ITEMS = [
        'ornament',
        'loom',
        'spool of cat6',
        'wreath',
        'fixed point',
        'shell',
        'candy cane',
        'weather machine'
    ]

    def __init__(self, computer: Computer, initial_commands: list, manual=False):
        self.computer = computer
        self.all_commands = []
        self.initial_commands = initial_commands
        self.manual = manual

    async def run(self):
        for com in self.initial_commands:
            await self.send_command(com)
        task = create_task(self.computer.execute())
        tried_comb = - 1
        while not self.computer.finished:
            if self.manual:
                await self.print_computer_output()
                await self.pass_manual_command()
            else:
                tried_comb += 1
                if tried_comb >= 1 << 9:
                    raise ValueError('Not found comb')
                for idx, item in enumerate(self.ALL_ITEMS):
                    if tried_comb & 1 << idx:
                        await self.send_command('drop %s' % item)
                await self.send_command('south')
                out = await self.print_computer_output()
                if ('Alert! Droids on this ship are lighter' not in out) and \
                   ('Alert! Droids on this ship are h' not in out):
                    return
                for idx, item in enumerate(self.ALL_ITEMS):
                    if tried_comb & 1 << idx:
                        await self.send_command('take %s' % item)

        task.cancel()

    async def print_computer_output(self):
        buffer = []
        while True:
            await sleep(0)
            buffer += [chr(c) for c in self.computer.flush_output()]
            buffer_str = ''.join(buffer)
            if buffer_str.endswith('Command?\n') or self.computer.finished:
                logger.info(buffer_str)
                return buffer_str

    async def pass_manual_command(self):
        manual_cmd = input('--> ')
        cmd = self.CMD_MAP.get(manual_cmd, manual_cmd)
        if cmd == 'history':
            logger.info('Commands history:\n%s', '\'%s\'' % '\', \''.join(self.all_commands))
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
        'north', 'take wreath', 'east', 'east', 'west', 'west', 'north', 'east', 'south', 'west', 'south', 'south', 'east', 'take loom', 'east', 'take fixed point', 'north', 'take spool of cat6', 'north', 'take weather machine', 'south', 'west', 'take shell', 'east', 'south', 'west', 'south', 'take ornament', 'east', 'south', 'east', 'west', 'south', 'north', 'north', 'west', 'west', 'north', 'take cany cane', 'north', 'inv', 'south', 'take candy cane', 'inv', 'south', 'east', 'north', 'west', 'north', 'north', 'east'
    ]
    gi = GameInterface(computer, initial_commands=INITIAL_COMMANDS, manual=False)
    await gi.run()


if __name__ == "__main__":
    init_logging()
    run_main_coroutine(main)
