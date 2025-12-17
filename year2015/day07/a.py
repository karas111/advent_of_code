import logging
import operator
import os
from abc import abstractmethod
from typing import Callable

from cachetools import cached

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Expression:
    @abstractmethod
    def execute(self, state: dict[str, "Expression"]) -> int: ...

    def _get_param(self, a: str, state: dict[str, "Expression"]) -> int:
        if a in state:
            return state[a].execute(state)
        return int(a)


class Const(Expression):
    def __init__(self, a: str):
        super().__init__()
        self._a = a

    @cached(cache={}, key=lambda self, state: self)
    def execute(self, state: dict[str, Expression]) -> int:
        return self._get_param(self._a, state)


class SingleArgsExpression(Expression):

    def __init__(self, a: str, op: Callable[[int], int]):
        super().__init__()
        self._a = a
        self._op = op

    @cached(cache={}, key=lambda self, state: self)
    def execute(self, state: dict[str, Expression]) -> int:
        val_a = self._get_param(self._a, state)
        return self._op(val_a)


class TwoArgsExpression(Expression):

    def __init__(self, a: str, b: str, op: Callable[[int, int], int]):
        super().__init__()
        self._a = a
        self._b = b
        self._op = op

    @cached(cache={}, key=lambda self, state: self)
    def execute(self, state: dict[str, Expression]) -> int:
        val_a = self._get_param(self._a, state)
        val_b = self._get_param(self._b, state)
        return self._op(val_a, val_b)


def read_input() -> dict[str, Expression]:
    res = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            inst_str, dest = line.strip().split(" -> ")
            inst = None
            match inst_str.split(" "):
                case a, "AND", b:
                    inst = TwoArgsExpression(a, b, operator.and_)
                case a, "OR", b:
                    inst = TwoArgsExpression(a, b, operator.or_)
                case a, "LSHIFT", b:
                    inst = TwoArgsExpression(a, b, operator.lshift)
                case a, "RSHIFT", b:
                    inst = TwoArgsExpression(a, b, operator.rshift)
                case "NOT", a:
                    inst = SingleArgsExpression(a, lambda x: (2 << 15) - x - 1)
                case val,:
                    inst = Const(val)
            res[dest] = inst
    return res


def main():
    state = read_input()
    res_a = state["a"].execute(state)
    logger.info("Res a: %s", res_a)

    state = read_input()
    state["b"] = Const(res_a)
    logger.info("Res b: %s", state["a"].execute(state))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
