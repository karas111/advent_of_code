import logging
import operator
import os
import random
import re
from dataclasses import dataclass
from itertools import combinations
from typing import Callable

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

OPS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}


@dataclass(frozen=True)
class ConstGate:
    out: str
    val: int

    def calculate(self, state):
        return self.val


@dataclass(frozen=True)
class Gate:
    a: str
    b: str
    op: str
    out: str

    def calculate(self, state) -> int:
        a = state[self.a].calculate(state)
        b = state[self.b].calculate(state)
        return OPS[self.op](a, b)


def read_input():
    gates = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        state = {}
        while l := f.readline().strip():
            name, val = l.split(": ")
            state[name] = ConstGate(name, int(val))

        pattern = re.compile(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)")
        while l := f.readline().strip():
            arg0, op, arg1, target = re.match(pattern, l).groups()
            state[target] = Gate(arg0, arg1, op, target)
            gates.append(state[target])
        return state, gates


def to_n(state: dict[str, Callable]) -> int:
    zs = []
    for i in range(45 + 1):
        zs.append(state[f"z{i:02d}"].calculate(state))
    res = "".join(str(x) for x in reversed(zs))
    return int(res, base=2)


def test(nbits: int, state: dict[str, Callable], n_iter=10000) -> bool:
    for _ in range(n_iter):
        x = random.randint(0, 1 << nbits)
        y = random.randint(0, 1 << nbits)
        for i in range(45):
            state[f"x{i:02d}"] = ConstGate(f"x{i:02d}", (x >> i) & 1)
            state[f"y{i:02d}"] = ConstGate(f"y{i:02d}", (y >> i) & 1)
        try:
            if (x + y) != to_n(state=state):
                return False
        except RecursionError:
            return False
    return True


def solve2(state: dict[str, Callable]):
    wrong = ["wpd", "z11", "jqf", "skh", "z19", "mdd", "z37", "wts"]
    current_state = dict(state)
    current_state["wpd"], current_state["z11"] = (
        current_state["z11"],
        current_state["wpd"],
    )
    current_state["jqf"], current_state["skh"] = (
        current_state["skh"],
        current_state["jqf"],
    )
    current_state["mdd"], current_state["z19"] = (
        current_state["z19"],
        current_state["mdd"],
    )
    current_state["z37"], current_state["wts"] = (
        current_state["wts"],
        current_state["z37"],
    )
    for nbits in range(45, 46):
        logger.info("Checking bits %d", nbits)
        if test(nbits, current_state):
            continue
        logger.info("Test for %d failed. Looking for bits to swap", nbits)
        for a, b in combinations(state.keys(), 2):
            if a in ("smt", "rhh") and b in ("smt", "rhh"):
                continue
            if a[0] in "xy" or b in "xy":
                continue
            # logger.info("Testing %s %s", a, b)
            n_state = dict(current_state)
            n_state[a], n_state[b] = n_state[b], n_state[a]
            if test(nbits, n_state):
                logger.info("Found thing to swap %s %s", a, b)
                current_state = n_state
                wrong.append(a)
                wrong.append(b)
                break
    return wrong


def get_wrong(gates: list[Gate], state: dict[str, Gate]):
    wrong = set()
    for gate in gates:
        if gate.out.startswith("z") and gate.op != "XOR" and gate.out != "z45":
            wrong.add(gate.out)
            continue
        if gate.op == "OR":
            if state[gate.a].op != "AND":
                wrong.add(gate.a)
            if state[gate.b].op != "AND":
                wrong.add(gate.b)
        if (
            gate.op == "XOR"
            and gate.out[0] not in "xyz"
            and gate.a[0] not in "xyz"
            and gate.b[0] not in "xyz"
        ):
            wrong.add(gate.out)

    return wrong


def main():
    state, gates = read_input()
    with catchtime(logger):
        # a = solve(x)
        logger.info("Res A: %s", to_n(state))
        wrong = get_wrong(gates, state)
        logger.info("wrong %s", wrong)
        b = solve2(state)
        logger.info("Res b: %s", ",".join(sorted(b)))


if __name__ == "__main__":
    init_logging()
    main()
