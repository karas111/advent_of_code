import heapq
import logging
import math
import os
from collections import deque
from typing import Callable, Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Monkey:

    def __init__(
        self,
        items: list[int],
        operation: str,
        test_div: int,
        true_monkey: int,
        false_monkey: int,
    ):
        self._items = deque(items)
        self._operation = operation
        self._test_div = test_div
        self._true_monkey = true_monkey
        self._false_monkey = false_monkey
        self.inspected = 0
        self._keep_small = lambda x: x // 3

    def set_kepp_small_modifier(self, keep_small: Callable[[int], int]):
        self._keep_small = keep_small

    def add_item(self, item: int) -> None:
        self._items.append(item)

    def play_turn(self) -> Iterable[tuple[int, int]]:
        while self._items:
            locals_ = {"old": self._items.popleft()}
            exec(self._operation, {}, locals_)
            new = locals_["new"]
            new = self._keep_small(new)
            to_monkey = self._inspect(new)
            yield (new, to_monkey)

    def _inspect(self, item: int) -> int:
        self.inspected += 1
        if item % self._test_div == 0:
            return self._true_monkey
        return self._false_monkey


def read_monkeys() -> list[Monkey]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        while f.readline():
            items = list(
                map(int, f.readline().strip().split("Starting items: ")[-1].split(", "))
            )
            operation = f.readline().strip().split("Operation: ")[-1]
            test_div = int(f.readline().strip().split("Test: divisible by ")[-1])
            true_monkey = int(
                f.readline().strip().split("If true: throw to monkey ")[-1]
            )
            false_monkey = int(
                f.readline().strip().split("If false: throw to monkey ")[-1]
            )
            f.readline()
            res.append(
                Monkey(
                    items=items,
                    operation=operation,
                    test_div=test_div,
                    true_monkey=true_monkey,
                    false_monkey=false_monkey,
                )
            )
    return res


def play_rounds(monkeys: list[Monkey], rounds: int):
    for _ in range(rounds):
        for monkey in monkeys:
            for item, to_monkey in monkey.play_turn():
                monkeys[to_monkey].add_item(item)


def main():
    monkeys = read_monkeys()
    play_rounds(monkeys, 20)
    inspected = [m.inspected for m in monkeys]
    a, b = heapq.nlargest(2, inspected)
    logger.info("Result a %s", a * b)

    monkeys = read_monkeys()
    modulo = math.prod(monkey._test_div for monkey in monkeys)

    def keep_small(x):
        return x % modulo

    for monkey in monkeys:
        monkey.set_kepp_small_modifier(keep_small)

    play_rounds(monkeys, 10000)
    inspected = [m.inspected for m in monkeys]
    logger.info(inspected)
    a, b = heapq.nlargest(2, inspected)
    logger.info("Result b %s", a * b)


if __name__ == "__main__":
    init_logging()
    main()
