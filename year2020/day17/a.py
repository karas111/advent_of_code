import itertools
import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    grid = set()
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    grid.add((x, y, 0))
    return grid


def do_one_step(grid, dimensions):
    DIMENSTIONS = dimensions

    def is_active(cords):
        deltas = set(itertools.product(*[(-1, 0, 1)] * DIMENSTIONS))
        deltas.remove((0,) * DIMENSTIONS)
        neighbours = sum(
            tuple(cords[i] + delta[i] for i in range(DIMENSTIONS)) in grid
            for delta in deltas
        )
        return (cords in grid and 2 <= neighbours <= 3) or (
            cords not in grid and neighbours == 3
        )

    ranges = []
    for dim in range(DIMENSTIONS):
        dim_val = [val[dim] for val in grid]
        ranges.append(range(min(dim_val) - 1, max(dim_val) + 2))

    new_grid = set()
    for cords in itertools.product(*ranges):
        if is_active(cords):
            new_grid.add(cords)

    return new_grid


def play_life(grid, max_rounds, dimensions):
    for i in range(max_rounds):
        grid = do_one_step(grid, dimensions)
    return grid


def main():
    grid = read_input()
    last_grid = play_life(grid, max_rounds=6, dimensions=3)
    logger.info(f"Res A={len(last_grid)}")
    grid = {val + (0,) for val in grid}
    last_grid = play_life(grid, max_rounds=6, dimensions=4)
    logger.info(f"Res B={len(last_grid)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
