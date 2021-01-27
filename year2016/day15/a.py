import functools
import logging
import os
import time
import re

from year2019.utils import init_logging
from year2020.day13.a import egcd

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    def parse_equation(line):
        args = re.match(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).", line).groups()
        args = [int(x) for x in args]
        return (args[1], (-args[0]-args[2]) % args[1])

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_equation(line.strip()) for line in f.readlines() if line]


def tcr(equations):
    current_mod, current_rest = equations[0]
    for mod, rest in equations[1:]:
        _, f, g = egcd(current_mod, mod)
        current_rest = (current_rest * g * mod + rest * f * current_mod) % (current_mod * mod)
        current_mod *= mod
    return current_mod, current_rest


def main():
    equations = parse_input()
    res = tcr(equations)
    logger.info(f"Res A {res[1]}")
    equations.append((11, (-len(equations) - 1) % 11))
    res_b = tcr(equations)
    logger.info(f"Res B {res_b[1]}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
