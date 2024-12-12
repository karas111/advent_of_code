from collections import deque
import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Cords = tuple[int, int]
Grid = dict[Cords, str]


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = {}
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line.strip()):
                res[(x, y)] = c
        return res


def calculate_corners(region: set[Cords]):
    fence_points = set()
    for x, y in region:
        fence_points.update([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)])

    def corner_n(cord: Cords) -> int:
        x, y = cord
        to_check_pairs = [
            ((x - 1, y - 1), (x, y - 1)),
            ((x, y - 1), (x, y)),
            ((x, y), (x - 1, y)),
            ((x - 1, y), (x - 1, y - 1)),
        ]
        matching_pairs = 0
        for a, b in to_check_pairs:
            matching_pairs += a in region and b in region

        # if 3 pairs are matching, then 4th should match as well
        assert matching_pairs != 3

        # if only one pair is matching then it's straight line
        # AA    AB
        # BB or AB
        if matching_pairs == 1:
            return 0

        # if all pairs are matching, then it is inner point
        # AA
        # AA
        if matching_pairs == 4:
            return 0

        # the other case is "inner conrer"
        # AB
        # AA
        if matching_pairs == 2:
            return 1

        # it means, it's either true corner or "X" shape double corner,
        # for example for region A
        # BB      AB
        # BA  vs  BA
        if matching_pairs == 0:
            if ((x - 1, y - 1) in region and (x, y) in region) or (
                (x, y - 1) in region and (x - 1, y) in region
            ):
                return 2
            else:
                return 1

    return sum(corner_n(cords) for cords in fence_points)


def bfs(g: Grid):
    visited_total = set()
    region_res = []

    def _bfs(start: Cords):
        queue = deque([start])
        region_visited = set()
        region_fence = 0
        while queue:
            current = queue.popleft()
            x, y = current
            if current in region_visited:
                continue
            region_visited.add(current)
            visited_total.add(current)
            for neighbour in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if g.get(neighbour) == g[current]:
                    queue.append(neighbour)
                else:
                    region_fence += 1
        return len(region_visited), region_fence, calculate_corners(region_visited)

    for cords in g:
        if cords not in visited_total:
            region_res.append(_bfs(cords))
    return region_res


def main():
    grid = read_input()
    with catchtime(logger):
        res = bfs(grid)
        logger.info("Res A: %s", sum(area * fence for area, fence, _ in res))
        logger.info("Res B: %s", sum(area * corners for area, _, corners in res))


if __name__ == "__main__":
    init_logging()
    main()
