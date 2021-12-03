import logging
import os
from typing import DefaultDict, List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_numbers():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def find_bit(numbers: List[str], n_bit: int, most_common: bool):
    count = sum(number[n_bit] == "1" for number in numbers)
    if (count > len(numbers) - count) ^ most_common:
        return "1"
    else:
        return "0"


def find_gamma_epsilon(numbers: List[str]):
    number_len = len(numbers[0])
    gamma = "".join([find_bit(numbers, n_bit=i, most_common=True) for i in range(number_len)])
    delta = "".join([find_bit(numbers, n_bit=i, most_common=False) for i in range(number_len)])
    return gamma, delta


# def find_co2_oxygen(numbers: List[str], gamma: str, delta: str):
#     res = copy.copy(numbers)
#     for bit in range(len(numbers[0])):


def main():
    numbers = read_numbers()
    gamma, delta = find_gamma_epsilon(numbers)
    logger.info(f"Result a {gamma}, {delta}, {int(gamma, base=2) * int(delta, base=2)}")
    # co2, oxygen = find_co2_oxygen(numbers, gamma, delta)


if __name__ == "__main__":
    init_logging()
    main()
