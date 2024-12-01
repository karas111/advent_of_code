import os
import logging
from typing import Dict, Iterable, List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_map() -> List[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]

def is_symbol(x, y, game, symbol_test=None) -> bool:
    if symbol_test is None:
        symbol_test = lambda c: not c.isnumeric() and c != "."
    if x < 0 or x >= len(game[0]):
        return False
    if y < 0 or y >= len(game):
        return False
    c = game[y][x]
    return symbol_test(c)

def check_n(y, min_x, max_x, game) -> bool:
    if is_symbol(min_x-1, y, game) or is_symbol(max_x, y, game):
        return True

    for x in range(min_x-1, max_x+1):
        for t_y in [y-1, y+1]:
            if is_symbol(x, t_y, game):
                return True
    return False

def get_numbers(game: List[Dict]) -> Iterable[int]:
    for y, line in enumerate(game):
        x = 0
        while x < len(line):
            if not line[x].isnumeric():
                x += 1
                continue
            min_x = x
            while x < len(line) and line[x].isnumeric():
                x += 1
            number = int(line[min_x: x])
            if check_n(y, min_x, x, game):
                yield number


def main():
    map_ = read_map()
    part_numbers = list(get_numbers(map_))
    logger.info(f"Result a {sum(part_numbers)}, {part_numbers}")



if __name__ == "__main__":
    init_logging()
    main()
