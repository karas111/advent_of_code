import logging

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def solve(row: int, column: int) -> int:
    full_diagonals = row + column - 2
    total_in_cycles = (1 + full_diagonals) * full_diagonals // 2
    nth = total_in_cycles + column
    return (20151125 * pow(252533, nth - 1, 33554393)) % 33554393


def main():
    logger.info("Res a: %s", solve(2947, 3029))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
