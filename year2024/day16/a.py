import logging
import os
from collections import deque
from typing import Iterable

from catch_time import catchtime
from graph.a_star import Graph, search_shortest
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

VECTORS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]
FINAL_GOAL_VEC_IDX = 4

Cords = tuple[int, int]
Node = tuple[Cords, int]
Path = tuple[Node, ...]


class Grid(Graph):
    def __init__(self, grid: list[str]):
        super().__init__()
        self._g = grid
        self.goal = self.find_point("E")

    def find_point(self, c: str) -> Cords:
        for y, line in enumerate(self._g):
            for x, other_c in enumerate(line):
                if other_c == c:
                    return (x, y)
        raise ValueError("Not found")

    def neighbours(self, n: Node, came_from=None) -> Iterable[tuple[Node, int]]:
        (x, y), move_idx = n
        dx, dy = VECTORS[move_idx]
        if (x, y) == self.goal:
            yield ((self.goal, FINAL_GOAL_VEC_IDX), 1)
            return
        n_x, n_y = x + dx, y + dy
        if self._g[n_y][n_x] != "#":
            yield (((n_x, n_y), move_idx), 1)
        yield (((x, y), (move_idx + 1) % len(VECTORS)), 1000)
        yield (((x, y), (move_idx - 1) % len(VECTORS)), 1000)


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return Grid([line.strip() for line in f])


def count_nodes(came_from: dict[Node, set[Node]], goal: Cords) -> int:

    already_visited = set()
    queue = deque()
    queue.append((goal, FINAL_GOAL_VEC_IDX))
    while queue:
        current = queue.popleft()
        if current in already_visited:
            continue
        already_visited.add(current)
        for neighbour in came_from[current]:
            queue.append(neighbour)
    visited_cords = {cords for cords, _ in already_visited}
    return len(visited_cords)


def main():
    g = read_input()
    with catchtime(logger):
        start_cords = g.find_point("S")
        start_node = (start_cords, 1)
        score, came_from = search_shortest(
            start_node, (g.goal, FINAL_GOAL_VEC_IDX), g, reconstruct_path=False
        )
        logger.info("Res A %s", score - 1)
        logger.info("Res B: %s", count_nodes(came_from, g.goal))


if __name__ == "__main__":
    init_logging()
    main()
