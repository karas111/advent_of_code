import logging
import os
from abc import abstractmethod
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Inst:
    CYCLES: int = -1

    @abstractmethod
    def execute(self, state: dict[str]) -> None: ...

    def __repr__(self):
        return str(type(self).__name__)


class NoOp(Inst):
    CYCLES: int = 1

    def execute(self, state: dict[str]) -> None: ...


class Addx(Inst):
    CYCLES: int = 2

    def __init__(self, n: int):
        super().__init__()
        self.n = n

    def execute(self, state: dict[str]):
        state["x"] += self.n

    def __repr__(self):
        return f"{super().__repr__()}({self.n})"


def read_inst() -> list[Inst]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            if line.strip() == "noop":
                res.append(NoOp())
            elif line.startswith("addx"):
                res.append(Addx(int(line.strip().split()[-1])))
    return res


def run_insts(insts: list[Inst], checkpoints: list[int]) -> Iterable[int]:
    cycle = 0  # finished cycle number
    state = {"x": 1}
    checkpoints = checkpoints[::-1]
    checkpoint = checkpoints.pop()
    for inst in insts:
        cycle += inst.CYCLES
        if cycle >= checkpoint:
            yield state["x"] * checkpoint
            if not checkpoints:
                return
            checkpoint = checkpoints.pop()
        inst.execute(state)


def run_insts_b(insts: list[Inst], cycle_stop=240) -> Iterable[str]:
    cycle = 0  # finished cycle number
    state = {"x": 1}
    for inst in insts:
        sprite_begin, sprite_end = state["x"] - 1, state["x"] + 1
        for _ in range(inst.CYCLES):
            if sprite_begin <= cycle % 40 <= sprite_end:
                yield "#"
            else:
                yield " "
            cycle += 1
        inst.execute(state)
        if cycle >= cycle_stop:
            return


def main():
    insts = read_inst()
    res = list(run_insts(insts, list(range(20, 221, 40))))
    logger.info("Result a %s", sum(res))
    res = list(run_insts_b(insts, 240))
    res = ["".join(res[i : i + 40]) for i in range(0, 240, 40)]
    logger.info("Result b\n%s", "\n".join(res))


if __name__ == "__main__":
    init_logging()
    main()
