import logging
import os
from typing import Callable

from pyparsing import deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> set[Cords]:
    res = set()
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                if c != "#":
                    res.add(Cords(x, y))
    return res


MOVES = [Cords(-1, 0), Cords(1, 0), Cords(0, -1), Cords(0, 1)]


def bfs(grid: set[Cords], start: Cords) -> dict[Cords]:
    distances = {}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node in distances:
            continue
        distances[node] = dist
        for dc in MOVES:
            nc = dc + node
            if nc in grid:
                queue.append((nc, dist + 1))
    return distances


def solve_a(grid: set[Cords]):
    l = max(c.x for c in grid) + 1
    start = Cords(l // 2, l // 2)
    distances = bfs(grid, start)
    return sum(dist <= 64 and dist % 2 == 0 for dist in distances.values())


def solve_b(grid: set[Cords], part_b: bool = False):
    l = max(c.x for c in grid) + 1
    mid = l // 2
    points = [Cords(x, y) for x in [0, mid, l - 1] for y in [0, mid, l - 1]]
    distances = {p: bfs(grid, p) for p in points}

    # assert max distance from the middle point is l // 2
    def count_distance(predicate: Callable[[int], bool], starting_point) -> int:
        return sum(predicate(v) for v in distances[starting_point].values())

    res = 0
    max_steps = 26501365
    n = (max_steps - mid) // l
    assert n == 202300

    # calculate full squares
    odd_full_sq = n**2
    even_full_sq = (n - 1) ** 2
    if n % 2 == 0:
        odd_full_sq, even_full_sq = even_full_sq, odd_full_sq
    res += count_distance(lambda v: v % 2 == 0, Cords(mid, mid)) * even_full_sq
    res += count_distance(lambda v: v % 2 == 1, Cords(mid, mid)) * odd_full_sq

    # calculate squares on vertexes
    # ..@..
    # .@@@.
    # @@@@@
    steps_left = max_steps - mid - (n - 1) * l - 1
    required_parity = steps_left % 2
    for p in [Cords(l - 1, mid), Cords(0, mid), Cords(mid, l - 1), Cords(mid, 0)]:
        res += count_distance(lambda v: v % 2 == required_parity and v <= steps_left, p)

    # calculate bigger squares on edges, where the corner triangle is "removed"
    # .@@
    # @@@
    # @@@
    steps_left_big = max_steps - 2 * mid - (n - 2) * l - 2
    required_parity_big = steps_left_big % 2
    on_edge_big_sq = n - 1
    for p in [Cords(l - 1, 0), Cords(l - 1, l - 1), Cords(0, l - 1), Cords(0, 0)]:
        res += (
            count_distance(
                lambda v: v % 2 == required_parity_big and v <= steps_left_big, p
            )
            * on_edge_big_sq
        )

    # calculate smaller squares on edges, where most part is cut and only triangle left
    # ...
    # ..@
    # .@@
    steps_left_small = max_steps - 2 * mid - (n - 1) * l - 2
    required_parity_small = steps_left_small % 2
    on_edge_small_sq = n
    for p in [Cords(l - 1, 0), Cords(l - 1, l - 1), Cords(0, l - 1), Cords(0, 0)]:
        res += (
            count_distance(
                lambda v: v % 2 == required_parity_small and v <= steps_left_small, p
            )
            * on_edge_small_sq
        )
    return res


def main():
    grid = read_input()
    res = solve_a(grid)
    logger.info("Res A: %d", res)
    res = solve_b(grid)
    logger.info("Res B: %d", res)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
