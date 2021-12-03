import logging
import os
from typing import List, NamedTuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_numbers():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def find_gamma_epsilon(numbers: List[str]):
    bit_count = [bit.count("0") for bit in zip(*numbers)]
    number_len = len(numbers)
    gamma = ["0" if x * 2 > number_len else "1" for x in bit_count]
    delta = ["0" if x == "1" else "1" for x in gamma]
    gamma = int("".join(gamma), base=2)
    delta = int("".join(delta), base=2)
    return gamma, delta


def main():
    numbers = read_numbers()
    gamma, delta = find_gamma_epsilon(numbers)
    logger.info(f"Result a {gamma}, {delta}, {gamma * delta}")


if __name__ == "__main__":
    init_logging()
    main()
