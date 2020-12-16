import logging
import os
import re
import time
from collections import namedtuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Mask = namedtuple("Mask", ["or_mask", "and_mask"])


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def create_mask(line) -> Mask:
    mask_str = line[len("mask = "):]
    return Mask(int(mask_str.replace("X", "0"), 2), int(mask_str.replace("X", "1"), 2))


def apply_mask_a(mask: Mask, value: int) -> int:
    value = value & mask.and_mask
    value = value | mask.or_mask
    return value


def adress_generator(mask_str: str, addr: int) -> int:
    floating_places = [i for i, char in enumerate(reversed(mask_str)) if char == "X"]
    mask = int(mask_str.replace("X", "0"), 2)
    for floating_values in range(1 << len(floating_places)):
        new_addr = mask | addr
        for floating_ord, floating_place in enumerate(floating_places):
            floating_bit = (floating_values >> floating_ord) & 1
            zero_bit = (1 << len(mask_str)) - 1 - (1 << floating_place)
            new_addr = (new_addr & zero_bit) | floating_bit << floating_place
        yield new_addr


def apply_mask_b(mask_str: str, addr: int, value: int, mem: dict) -> dict:
    addresses = list(adress_generator(mask_str, addr))
    for addr in addresses:
        mem[addr] = value
    return mem


def run_instructions(instructions, part_b=False):
    mem = {}
    mask = None
    for instruction in instructions:
        if "mask = " in instruction:
            if part_b:
                mask = instruction[len("mask = "):]
            else:
                mask = create_mask(instruction)
        else:
            addr, value = [
                int(x)
                for x in re.match(r"^mem\[(\d+)\] = (\d+)$", instruction).groups()
            ]
            if part_b:
                mem = apply_mask_b(mask, addr, value, mem)
            else:
                value = apply_mask_a(mask, value)
                mem[addr] = value
    return mem


def main():
    instructions = read_input()
    mem = run_instructions(instructions)
    logger.info(f"Res A={sum(mem.values())}")
    mem = run_instructions(instructions, part_b=True)
    logger.info(f"Res B={sum(mem.values())}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
