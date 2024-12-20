import logging
import os
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable

from catch_time import catchtime
from cords.cords_2d import Cords
from graph import a_star
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVE_VEC = [
    Cords(1, 0),
    Cords(0, 1),
    Cords(-1, 0),
    Cords(0, -1),
]


@dataclass(frozen=True)
class Node:
    cords: Cords
    move_vec: int


class LavaGrid(a_star.Graph):
    def __init__(self, weights: dict[Cords, int], min_dist: int, max_dist: int):
        self._weights = weights
        self._min_dist = min_dist
        self._max_dist = max_dist

    @cached_property
    def start(self) -> Node:
        return Node(Cords(0, 0), 4)

    @cached_property
    def end(self) -> Node:
        max_x = max(c.x for c in self._weights)
        max_y = max(c.y for c in self._weights)
        return Node(Cords(max_x, max_y), -1)

    def neighbours(self, n: Node) -> Iterable[tuple[Node, int]]:
        if n.cords == self.end.cords:
            yield (self.end, 1)
            return

        for new_move_vec in range(4):
            if n.move_vec == new_move_vec or (n.move_vec + 2) % 4 == new_move_vec:
                continue
            vec = MOVE_VEC[new_move_vec]
            cost_increase = 0
            for dist in range(1, self._max_dist + 1):
                new_cords = n.cords + vec * dist
                if new_cords not in self._weights:
                    break
                cost_increase += self._weights[new_cords]
                if dist < self._min_dist:
                    continue
                yield (Node(new_cords, new_move_vec), cost_increase)


def read_input() -> dict[Cords, int]:
    nodes = {}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                nodes[Cords(x, y)] = int(c)
        return nodes


def main():
    g = read_input()
    with catchtime(logger):
        lg = LavaGrid(g, 1, 3)
        l, _ = a_star.search_shortest(lg.start, lg.end, lg)
        logger.info("Res A: %s", l - 1)
        # logger.info("\n".join(str(x) for x in path))
        lg = LavaGrid(g, 4, 10)
        l, _ = a_star.search_shortest(lg.start, lg.end, lg)
        logger.info("Res B: %s", l - 1)


if __name__ == "__main__":
    init_logging()
    main()
