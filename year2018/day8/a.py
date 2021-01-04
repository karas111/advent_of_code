import datetime
import logging
import os
import re
import time
from collections import namedtuple
from enum import Enum
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class LinkedList:
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def create(cls, args, circle=False) -> 'LinkedList':
        nodes = [cls(arg) for arg in args]
        for i in range(len(nodes) - 1):
            nodes[i].connect(nodes[i+1])
        if circle:
            nodes[-1].connect(nodes[0])
        return nodes[0]

    def connect(self, other: 'LinkedList'):
        self.right = other
        other.left = self

    def rotate(self, n, left=False) -> 'LinkedList':
        curr = self
        for _ in range(n):
            if left:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def __str__(self) -> str:
        curr = self.right
        seen = {self}
        res = [self.val]
        while curr is not None and curr not in seen:
            res.append(curr.val)
            seen.add(curr)
            curr = curr.right
        return str(res)


def play(players, stones):
    queue = list(range(stones, 0, -1))
    scores = {i: 0 for i in range(players)}
    current = LinkedList.create([0], circle=True)
    player = 0
    while queue:
        stone = queue.pop()
        if stone % 23 == 0:
            to_remove = current.rotate(7, left=True)
            left, right = to_remove.left, to_remove.right
            current = right
            scores[player] += stone + to_remove.val
            left.connect(right)
            # queue.append(to_remove.val)
        else:
            node = LinkedList(stone)
            left, right = current.right, current.right.right
            left.connect(node)
            node.connect(right)
            current = node
        player = (player + 1) % players
    return scores


def main():
    # players, stones = 9, 25
    players, stones = 13, 7999
    players, stones = 425, 70848
    scores = play(players, stones)
    logger.info(f"Res A {max(scores.values())}")
    scores = play(players, stones*100)
    logger.info(f"Res B {max(scores.values())}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
