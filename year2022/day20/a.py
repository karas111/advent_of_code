import logging
import os
from dataclasses import dataclass
from typing import Optional

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_file() -> list[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [int(line.strip()) for line in f]


@dataclass
class Node:
    val: int
    prev: Optional["Node"] = None
    next: Optional["Node"] = None

    def __repr__(self):
        return f"Node({self.val})"


def mix(numbers: list[int], rounds: int = 1) -> list[int]:
    l = len(numbers)
    dll = [Node(n) for n in numbers]
    for i in range(l):
        dll[i].prev = dll[(i - 1) % l]
        dll[i].next = dll[(i + 1) % l]

    for _ in range(rounds):
        for node in dll:
            # take out the node
            insert_after = node.prev
            node.prev.next, node.next.prev = node.next, node.prev
            # find where to put it back
            for _ in range(node.val % (l - 1)):
                insert_after = insert_after.next
            insert_before = insert_after.next
            # put it back
            insert_after.next, insert_before.prev = node, node
            node.prev, node.next = insert_after, insert_before

    node = dll[0]
    res = []
    for _ in range(l):
        res.append(node.val)
        node = node.next
    return res


def get_result(numbers: list[int]) -> int:
    idx = numbers.index(0)
    return sum(numbers[(idx + i) % len(numbers)] for i in range(1000, 3001, 1000))


def main():
    numbers = read_file()
    mixed = mix(numbers)
    logger.info("Result a %s", get_result(mixed))

    numbers = [n * 811589153 for n in numbers]
    mixed = mix(numbers, rounds=10)
    logger.info("Result b %s", get_result(mixed))


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
