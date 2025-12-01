import logging
import operator
import os
import re
from collections import namedtuple

from sympy import Eq, symbols
from sympy.solvers import solve

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Operation = namedtuple("Operation", "a op b")


def read_input() -> tuple[dict[str, int], dict[str, Operation]]:
    int_pattern = r"(\w+): (-?\d+)"
    op_pattern = r"(\w+): (\w+) ([+\-*/]) (\w+)"
    calculated = {}
    operations = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.strip()
            if m := re.match(int_pattern, line):
                calculated[m.groups()[0]] = int(m.groups()[1])
            else:
                m = re.match(op_pattern, line)
                operations[m.groups()[0]] = Operation(*m.groups()[1:])

        return calculated, operations


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(
    monkey: str, calculated: dict[str, int], operations: dict[str, Operation]
) -> int:
    if monkey not in calculated:
        op = operations[monkey]
        calculated[monkey] = OPERATORS[op.op](
            calculate(op.a, calculated, operations),
            calculate(op.b, calculated, operations),
        )
    return calculated[monkey]


def part_b(calcualted: dict[str, int], operations: dict[str, Operation]) -> int:
    humn = symbols("humn")
    calcualted["humn"] = humn
    root = operations.pop("root")
    left = calculate(root.a, calcualted, operations)
    right = calculate(root.b, calcualted, operations)
    res = solve(Eq(left, right))
    return round(res[0])


def main():
    calculated, operations = read_input()
    logger.info("Result a %d", calculate("root", calculated, operations))
    calculated, operations = read_input()
    logger.info("Result a %d", part_b(calculated, operations))


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
