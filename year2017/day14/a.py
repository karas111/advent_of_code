import logging
import time

from year2017.day10.a import knot_hash_str
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def create_grid(key):
    res = []
    for i in range(128):
        row_key = f"{key}-{i}"
        knot_hash = knot_hash_str(row_key)
        bin_repr = format(int(knot_hash, 16), "0128b")
        res.append([int(x) for x in bin_repr])
    return res


def find_region(grid, i, j):
    region = set()
    queue = [(i, j)]
    while queue:
        x, y = queue.pop()
        if (x, y) in region:
            continue
        region.add((x, y))
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 128 and 0 <= ny < 128 and grid[nx][ny]:
                queue.append((nx, ny))
    return region


def find_regions(grid):
    seen = set()
    regions = []
    for i in range(128):
        for j in range(128):
            if grid[i][j] and (i, j) not in seen:
                region = find_region(grid, i, j)
                seen = seen | region
                regions.append(region)
    return regions


def main():
    key = "hfdlxzhv"
    # key = "flqrgnkx"
    grid = create_grid(key)
    logger.info(f"Res A {sum(sum(line) for line in grid)}")
    regions = find_regions(grid)
    logger.info(f"Res B {len(regions)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
