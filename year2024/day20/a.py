import logging
import os
from collections import defaultdict, deque

from catch_time import catchtime
from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Grid = list[str]

MOVE_VEC = [
    Cords(1, 0),
    Cords(-1, 0),
    Cords(0, 1),
    Cords(0, -1),
]


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [l.strip() for l in f]


def find_node(g: Grid, c: str) -> Cords:
    for y, line in enumerate(g):
        for x, c_ in enumerate(line):
            if c == c_:
                return Cords(x, y)
    raise ValueError(f"Not found {c}")


def bfs(g: Grid, start: Cords) -> dict[Cords, int]:
    queue = deque([(start, 0)])
    depths = {}
    while queue:
        current, depth = queue.popleft()
        if current in depths:
            continue
        depths[current] = depth
        for dv in MOVE_VEC:
            neighbour = current + dv
            if g[neighbour.y][neighbour.x] != "#":
                queue.append((neighbour, depth + 1))
    return depths


def solve(g: Grid, max_cheat_size: int) -> int:
    start = find_node(g, "S")
    end = find_node(g, "E")
    start_depths = bfs(g, start)
    end_depths = bfs(g, end)
    shortest_path = start_depths[end]
    res = defaultdict(int)
    for cheat_start, depth_from_start in start_depths.items():
        for add_x in range(-max_cheat_size, max_cheat_size + 1):
            max_add_y = max_cheat_size - abs(add_x)
            for add_y in range(-max_add_y, max_add_y + 1):
                cheat_end = Cords(cheat_start.x + add_x, cheat_start.y + add_y)
                if cheat_end not in start_depths:
                    continue
                new_shortest = (
                    abs(add_x) + abs(add_y) + depth_from_start + end_depths[cheat_end]
                )
                if new_shortest < shortest_path:
                    res[shortest_path - new_shortest] += 1
    return sum(v for k, v in res.items() if k >= 100)


def main():
    g = read_input()
    with catchtime(logger):
        res = solve(g, max_cheat_size=2)
        logger.info("Res A: %s", res)
        res = solve(g, max_cheat_size=20)
        logger.info("Res B: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
