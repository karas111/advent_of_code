import itertools
import logging
import os
from typing import Iterable


from year2019.utils import init_logging
from graph.a_star import search_shortest, Graph

INPUT_FILE = "input.txt"

logger = logging.getLogger(__name__)

Cords = tuple[int, int]
Nodes = set[Cords]


class Grid(Graph):
    def __init__(self, nodes):
        super().__init__()
        self._nodes = nodes

    def neighbours(self, n: Cords) -> Iterable[tuple[Cords, int]]:
        x, y = n
        for neighbour in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if neighbour in self._nodes:
                yield neighbour, 1


def read_input() -> tuple[Grid, list[Cords]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        graph = set()
        starting_points = [None] * 10
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                if c != "#":
                    graph.add((x, y))
                if c.isdigit():
                    starting_points[int(c)] = (x, y)
        starting_points = list(filter(lambda n: n is not None, starting_points))
        return Grid(graph), starting_points


def main():
    grid, starting_pos = read_input()
    paths = {}
    for idx, a in enumerate(starting_pos):
        for b in starting_pos[idx + 1 :]:
            path_l, _ = search_shortest(a, b, grid)
            paths[(a, b)] = paths[(b, a)] = path_l
    to_visit = starting_pos[1:]
    best_a, best_b = 10**12, 10**12
    for perm in itertools.permutations(to_visit):
        all_nodes = [starting_pos[0]] + list(perm) + [starting_pos[0]]
        perm_res = [paths[(a, b)] for a, b in zip(all_nodes, all_nodes[1:])]
        best_a = min(best_a, sum(perm_res[:-1]))
        best_b = min(best_b, sum(perm_res))
    logger.info("Res a %s", best_a)
    logger.info("Res b %s", best_b)


if __name__ == "__main__":
    init_logging()
    main()
