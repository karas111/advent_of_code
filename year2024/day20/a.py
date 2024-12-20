import logging
import os
from collections import defaultdict, deque
from itertools import product

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
    for cheat_s_x, cheat_s_y in product(range(1, len(g[0]) - 1), range(1, len(g) - 1)):
        cheat_start = Cords(cheat_s_x, cheat_s_y)
        if g[cheat_start.y][cheat_start.x] == "#":
            continue
        for cheat_size in range(2, max_cheat_size + 1):
            for add_x in range(cheat_size + 1):
                seen_cheat_end = set()
                for mult_x, mult_y in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
                    cheat_end = Cords(
                        cheat_s_x + add_x * mult_x,
                        cheat_s_y + (cheat_size - add_x) * mult_y,
                    )
                    if cheat_end in seen_cheat_end:
                        continue
                    seen_cheat_end.add(cheat_end)
                    if (
                        cheat_end.x < 0
                        or cheat_end.x >= len(g[0])
                        or cheat_end.y < 0
                        or cheat_end.y >= len(g)
                        or g[cheat_end.y][cheat_end.x] == "#"
                    ):
                        continue
                    new_shortest = (
                        cheat_size + start_depths[cheat_start] + end_depths[cheat_end]
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
