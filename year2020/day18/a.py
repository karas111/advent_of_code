import itertools
import logging
import os
import time
from typing import NamedTuple, List, Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Expression:
    def execute() -> int:
        raise NotImplementedError()


class Operation(Expression):
    def __init__(self, arg1: Expression, arg2: Expression, op: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2
        self.op = op

    def execute(self) -> int:
        if self.op == "+":
            return self.arg1.execute() + self.arg2.execute()
        elif self.op == "*":
            return self.arg1.execute() * self.arg2.execute()
        raise ValueError("Wrong operator")


class IntExpr(Expression):
    def __init__(self, number):
        self.number = number

    def execute(self) -> int:
        return self.number


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line]


def parse_parenthesis(symbols, idx, part_b) -> Tuple[Expression, int]:
    idx += 1  # skip )
    expr = None
    while symbols[idx] != "(":
        expr, idx = parse_expression(symbols, idx, arg1=expr, nested_op=None, part_b=part_b)
    idx += 1  # skip (
    return expr, idx


def parse_expression(symbols: List[str], idx: int, arg1=None, nested_op=None, part_b=False) -> Tuple[Expression, int]:
    symbol = symbols[idx]
    if arg1 is None:
        if symbol == ")":
            arg1, idx = parse_parenthesis(symbols, idx, part_b)
        else:
            arg1 = IntExpr(int(symbol))
            idx += 1
    if idx >= len(symbols) or symbols[idx] == "(":
        return arg1, idx
    if nested_op == "+" and symbols[idx] == "*" and part_b:
        return arg1, idx
    op = symbols[idx]
    idx += 1
    arg2, idx = parse_expression(symbols, idx, nested_op=op, part_b=part_b)
    return Operation(arg1, arg2, op), idx


def parse_line(line, part_b) -> Expression:
    symbols = list(reversed(line.replace("(", "( ").replace(")", " )").split(" ")))
    res = None
    idx = 0
    while idx < len(symbols):
        res, idx = parse_expression(symbols, idx=idx, arg1=res, part_b=part_b)
    return res


def main():
    exprs_str = read_input()
    exprs = [parse_line(expr_str, part_b=False) for expr_str in exprs_str]
    vals = [expr.execute() for expr in exprs]
    logger.info(f"Res {vals}, A={sum(vals)}")
    exprs = [parse_line(expr_str, part_b=True) for expr_str in exprs_str]
    vals = [expr.execute() for expr in exprs]
    logger.info(f"Res {vals}, B={sum(vals)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
