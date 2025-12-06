import logging
import os
from collections import defaultdict

from pyparsing import deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOVES = {"^": Cords(0, -1), "v": Cords(0, 1), "<": Cords(-1, 0), ">": Cords(1, 0)}


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def reduce_graph(grid: list[str], start: Cords, end: Cords, slippery: bool) -> int:
    vertexes = {start, end}
    for y, line in enumerate(grid[1:-1]):
        for x, c in enumerate(line[1:-1]):
            if c == "#":
                continue
            cords = Cords(x + 1, y + 1)
            n_neighbours = 0
            for d_c in MOVES.values():
                neighbour = cords + d_c
                n_neighbours += grid[neighbour.y][neighbour.x] != "#"
            if n_neighbours > 2:
                vertexes.add(cords)

    edges = defaultdict(list)

    for source in vertexes:
        queue = deque([(source, 0)])
        seen = set()
        while queue:
            node, dist = queue.popleft()
            if node in seen:
                continue
            seen.add(node)
            if source != node and node in vertexes:
                edges[source].append((node, dist))
                continue

            to_check = MOVES
            c = grid[node.y][node.x]
            if slippery and c != ".":
                to_check = [c]
            for direction in to_check:
                n_c = node + MOVES[direction]
                if (
                    0 <= n_c.x < len(grid[0])
                    and 0 <= n_c.y < len(grid)
                    and grid[n_c.y][n_c.x] != "#"
                ):
                    queue.append((n_c, dist + 1))
    return edges


def solve(edges: dict[Cords, list[Cords]], start: Cords, end: Cords) -> int:
    seen = set()
    valid_paths_l = []

    def dfs(node: Cords, dist: int):
        if node in seen:
            return
        if node == end:
            valid_paths_l.append(dist)
            return
        seen.add(node)
        for neighbour, dist_n in edges[node]:
            dfs(neighbour, dist + dist_n)
        seen.remove(node)

    dfs(start, 0)
    return max(valid_paths_l)


def main():
    grid = read_input()
    start, end = Cords(1, 0), Cords(len(grid[0]) - 2, len(grid) - 1)
    edges = reduce_graph(grid, start, end, slippery=True)
    res = solve(edges, start, end)
    logger.info("Res a: %d", res)

    edges = reduce_graph(grid, start, end, slippery=False)
    res = solve(edges, start, end)
    logger.info("Res b: %d", res)


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
