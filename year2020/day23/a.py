import logging
import time
from typing import Dict

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class LinkedList:
    def __init__(self, val) -> None:
        self.val = val
        self.right = None

    @staticmethod
    def create(args):
        size = len(args)
        nodes = [LinkedList(v) for v in args]
        for i in range(size):
            nodes[i].right = nodes[(i + 1) % size]
        return {n.val: n for n in nodes}

    def to_list(self):
        res = [self.val]
        current = self
        while (current := current.right) != self:
            res.append(current.val)
        return res


def get_destination(deck: Dict[int, LinkedList], current: LinkedList):
    cut = [current.right.val, current.right.right.val, current.right.right.right.val]
    new_val = (current.val - 1) or len(deck)
    while new_val in cut:
        new_val = (new_val - 1) or len(deck)
    return deck[new_val]


def play(deck: Dict[int, LinkedList], current: int, rounds: int):
    current_node = deck[current]
    while rounds > 0:
        first_cut, last_cut = current_node.right, current_node.right.right.right
        destination_start = get_destination(deck, current_node)
        destination_end = destination_start.right
        current_node.right = last_cut.right
        destination_start.right = first_cut
        last_cut.right = destination_end
        current_node = current_node.right
        if rounds % 10 ** 6 == 0:
            logger.info(f"Rounds left {rounds}")
        rounds -= 1


def main():
    init_deck = [4, 6, 7, 5, 2, 8, 1, 9, 3]
    # init_deck = [int(x) for x in "389125467"]
    deck = LinkedList.create(init_deck)
    play(deck, current=init_deck[0], rounds=100)
    res_a = "".join([str(x) for x in deck[1].to_list()[1:]])
    logger.info(f"Res A {res_a}")

    init_deck += list(range(10, 10 ** 6 + 1))
    deck = LinkedList.create(init_deck)
    play(deck, current=init_deck[0], rounds=10 ** 7)
    node = deck[1]
    logger.info(f"Res B {node.right.val * node.right.right.val}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
