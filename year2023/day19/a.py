import logging
import operator
import os
import re
from math import prod
from typing import Optional

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


OPERATORS = {"<": operator.lt, ">": operator.gt}


def split_range(r: range, split_point: int):
    first = range(r.start, min(r.stop, split_point)) or None
    second = range(max(r.start, split_point), r.stop) or None
    return first, second


class Rule:
    def __init__(self, condition: str):
        c = condition.split(":")
        self.target = c[-1]
        if len(c) == 1:
            self._operator = None
            self._arg0 = None
            self._arg1 = None
        else:
            self._operator = OPERATORS[c[0][1]]
            self._arg0 = c[0][0]
            self._arg1 = int(c[0][2:])

    def eval_rule(self, obj: dict[str, int]) -> Optional[str]:
        if self._operator is None:
            return self.target
        if self._operator(obj[self._arg0], self._arg1):
            return self.target
        return None

    def eval_ranges(self, objs: list[dict[str, range]]):
        if self._operator is None:
            return objs, []
        accepted, rejected = [], []
        for obj in objs:
            param_r = obj[self._arg0]
            start, end = split_range(
                param_r, self._arg1 + (self._operator == operator.gt)
            )
            if self._operator == operator.lt:
                accepted_range, rejected_range = start, end
            else:
                accepted_range, rejected_range = end, start
            if accepted_range:
                accepted.append({**obj, self._arg0: accepted_range})
            if rejected_range:
                rejected.append({**obj, self._arg0: rejected_range})
        return accepted, rejected

    def __repr__(self):
        return f"Rule({self._arg0} {self._operator.__name__} {self._arg1} -> {self._target})"


def read_input() -> tuple[dict[str, list[Rule]], list[dict[str, int]]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(r"(\w+)\{(.+)\}")
        pipes = {}
        while line := f.readline().strip():
            pipe, rules_str = re.match(pattern, line).groups()
            pipes[pipe] = [Rule(r) for r in rules_str.split(",")]

        objs = []
        while line := f.readline().strip():
            line = line.replace("{", "dict(")
            line = line.replace("}", ")")
            objs.append(eval(line))
        return pipes, objs


def solve(
    pipes: dict[str, list[Rule]], objs: list[dict[str, int]], part2: bool = False
):

    def _solve_rule(current_pipe: str, obj: dict[str, int]) -> bool:
        for rule in pipes[current_pipe]:
            target = rule.eval_rule(obj)
            if target is None:
                continue
            if target == "A":
                return True
            if target == "R":
                return False
            return _solve_rule(target, obj)

    if not part2:
        return sum(sum(obj.values()) for obj in objs if _solve_rule("in", obj))


def solve2(pipes: dict[str, list[Rule]]):
    obj = {k: range(1, 4001) for k in "xmas"}
    accepted = []

    def _solve_rule(current_pipe: str, objs: list[dict[str, range]]):
        for rule in pipes[current_pipe]:
            rule_accepted, rule_rejected = rule.eval_ranges(objs)
            if rule.target == "A":
                accepted.extend(rule_accepted)
            elif rule.target != "R":
                _solve_rule(rule.target, rule_accepted)
            objs = rule_rejected

    _solve_rule("in", [obj])
    res = 0
    for obj in accepted:
        res += prod(len(v) for v in obj.values())
    return res


def main():
    pipes, objs = read_input()
    with catchtime(logger):
        logger.info("Res A: %s", solve(pipes, objs))
        logger.info("Res B: %s", solve2(pipes))


if __name__ == "__main__":
    init_logging()
    main()
