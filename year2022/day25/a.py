import logging
import os
from typing import NamedTuple

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


VALUES = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}
VALUES_REV = {v: k for k, v in VALUES.items()}


def convert_from(n_str: str) -> int:
    res = 0
    for digit in n_str:
        res *= 5
        res += VALUES[digit]
    return res


def convert_to(n: int) -> str:
    digits = []
    modifier = 0
    while n:
        current_dig = n % 5
        current_dig += modifier
        modifier = 0
        if current_dig > 2:
            current_dig = current_dig - 5
            modifier = 1
        digits.append(current_dig)
        n //= 5
    if modifier:
        digits.append(modifier)
    return "".join(VALUES_REV[d] for d in reversed(digits))


def main():
    numbers = read_input()
    res = [convert_from(n) for n in numbers]
    logger.info("Res a: %s", convert_to(sum(res)))


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
