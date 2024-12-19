import logging
import os
from functools import cache

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> tuple[list[str], list[str]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        patterns = f.readline().strip().split(", ")
        f.readline()
        designs = [line.strip() for line in f]
        return patterns, designs


def count_possible(
    patterns: list[str], designs: list[str], count_combination: bool
) -> int:
    aggr = sum if count_combination else any

    @cache
    def n_possible(design: str) -> int:
        if design == "":
            return True
        return aggr(
            design.startswith(pattern) and n_possible(design[len(pattern) :])
            for pattern in patterns
        )

    return sum(n_possible(design) for design in designs)


def main():
    pattern, designs = read_input()
    with catchtime(logger):
        res = count_possible(pattern, designs, count_combination=False)
        logger.info("Res A: %s", res)
        res = count_possible(pattern, designs, count_combination=True)
        logger.info("Res A: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
