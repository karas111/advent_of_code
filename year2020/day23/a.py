import itertools
import logging
import os
import time
from collections import deque
from typing import Deque, Tuple, Dict

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class LinkedList:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def create(args):
        size = len(args)
        nodes = [LinkedList(v) for v in args]
        for i in range(size):
            nodes[i].left, nodes[i].right = nodes[(i-1)%size], nodes[(i+1) % size]
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
        destination = get_destination(deck, current_node)
        current_node.right, last_cut.right.left = last_cut.right, current_node
        last_cut.right, destination.right.left = destination.right, last_cut
        destination.right, first_cut.left = first_cut, destination
        current_node = current_node.right
        rounds -= 1
        # print(rounds)


def main():
    init_deck = [4, 6, 7, 5, 2, 8, 1, 9, 3]
    init_deck = [int(x) for x in "389125467"]
    deck = LinkedList.create(init_deck)
    # print(deck[4].to_list())
    play(deck, current=init_deck[0], rounds=1)
    print(deck[1].to_list())



if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
