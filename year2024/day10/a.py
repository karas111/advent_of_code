from collections import defaultdict
from dataclasses import dataclass
import logging
import os
from typing import DefaultDict


from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Map = dict[tuple[int, int], int]

START_VAL = 0
END_VAL = 9


@dataclass
class PointRes:
    reached_tops: set[tuple[int, int]]
    paths_to_tops: int


def read_input() -> Map:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.readlines()
        res = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                res[(x, y)] = int(c)
    return res


def dfs(m: Map):

    res: DefaultDict[tuple[int, int], PointRes] = defaultdict(
        lambda: PointRes(set(), 0)
    )
    visited = defaultdict(lambda: False)

    def _dfs(current: tuple[int, int]):
        if visited[current]:
            return
        visited[current] = True
        if m[current] == END_VAL:
            res[current].paths_to_tops = 1
            res[current].reached_tops = {current}
        x, y = current
        for neighbour in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if neighbour not in m or m[neighbour] != m[current] + 1:
                continue
            _dfs(neighbour)
            res[current].paths_to_tops += res[neighbour].paths_to_tops
            res[current].reached_tops |= res[neighbour].reached_tops

    starting_positions = [pos for pos, val in m.items() if val == START_VAL]
    for starting_position in starting_positions:
        _dfs(starting_position)
    res_a = sum(len(res[start].reached_tops) for start in starting_positions)
    logger.info("Res A %s", res_a)
    res_b = sum(res[start].paths_to_tops for start in starting_positions)
    logger.info("Res B %s", res_b)

    return res


def main():
    m = read_input()
    with catchtime(logger):
        dfs(m)


if __name__ == "__main__":
    init_logging()
    main()
