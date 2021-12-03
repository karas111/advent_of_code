import logging
import os
import copy
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_numbers():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def find_bit(numbers: List[str], n_bit: int, most_common: bool):
    count = sum(number[n_bit] == "1" for number in numbers)
    if count == len(numbers) - count:
        return most_common and "1" or "0"
    elif (count > len(numbers) - count) ^ most_common:
        return "0"
    else:
        return "1"


def find_gamma_epsilon(numbers: List[str]):
    number_len = len(numbers[0])
    gamma = "".join(
        [find_bit(numbers, n_bit=i, most_common=True) for i in range(number_len)]
    )
    delta = "".join(
        [find_bit(numbers, n_bit=i, most_common=False) for i in range(number_len)]
    )
    return gamma, delta


def filter_air(numbers: List[str], most_common: bool):
    res = copy.copy(numbers)
    n_bit = 0
    while len(res) > 1:
        v_bit = find_bit(res, n_bit=n_bit, most_common=most_common)
        res = [number for number in res if number[n_bit] == v_bit]
        n_bit += 1
    return res[0]


def main():
    numbers = read_numbers()
    gamma, delta = find_gamma_epsilon(numbers)
    logger.info(f"Result a {gamma}, {delta}, {int(gamma, base=2) * int(delta, base=2)}")
    ox, co2 = filter_air(numbers, most_common=True), filter_air(numbers, most_common=False)
    logger.info(f"Result b {ox}, {co2}, {int(ox, base=2) * int(co2, base=2)}")


if __name__ == "__main__":
    init_logging()
    main()
