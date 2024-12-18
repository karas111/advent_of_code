import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Grid = list[list[str]]


def read_input() -> Grid:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [list(l.strip()) for l in f]


def count_load(g: Grid) -> int:
    return sum(row.count("O") * (len(g) - y) for y, row in enumerate(g))


def slide(g: Grid) -> Grid:
    for x, column in enumerate(zip(*g)):
        last_taken_idx = -1
        for y, c in enumerate(column):
            if c == "#":
                last_taken_idx = y
            elif c == "O":
                last_taken_idx += 1
                g[y][x] = "."
                g[last_taken_idx][x] = "O"
    return g


def spin_cycle(g: Grid, n_iter: int) -> Grid:
    seen = []
    first_repeat = -1
    n_cycles = 0
    score = []
    while True:
        for _ in range(4):
            g = slide(g)
            g = [list(l) for l in zip(*g[::-1])]
        score.append(count_load(g))
        # logger.info("\n%s", "\n".join("".join(l) for l in g))
        if first_repeat > 0 and g == seen[first_repeat]:
            logger.info(
                "Cycle start at %d and have length of %d",
                first_repeat,
                n_cycles - first_repeat,
            )
            break
        if first_repeat < 0 and g in seen:
            first_repeat = n_cycles
            logger.info("Repeating first time at %d", first_repeat)
        seen.append([list(l) for l in g])
        n_cycles += 1

    offset_in_cycle = (n_iter - first_repeat) % (n_cycles - first_repeat)
    return score[first_repeat - 1 + offset_in_cycle]


def main():
    g = read_input()
    with catchtime(logger):
        g = slide(g)
        logger.info("Res A: %s", count_load(g))
        b = spin_cycle(g, 1000000000)
        logger.info("Res B %d", b)


if __name__ == "__main__":
    init_logging()
    main()
