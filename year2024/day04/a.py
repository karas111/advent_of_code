import logging
import os
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_words() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_count(line: str, pattern: str = "XMAS") -> int:
    return line.count(pattern)


def generate_lines(words: list[str]) -> Iterable[str]:
    top_points = {(x, 0) for x in range(len(words[0]))}
    bottom_points = {(x, len(words) - 1) for x in range(len(words[0]))}
    left_points = {(0, y) for y in range(len(words))}
    # right_points = {(len(words[0]) -1, y) for y in range(len(words))}
    line_generator = {
        # horizontal
        (1, 0): left_points,
        # vertical
        (0, 1): top_points,
        # diagonal /
        (1, -1): bottom_points | left_points,
        # diagonal \
        (1, 1): top_points | left_points,
    }
    for (dx, dy), starting_points in line_generator.items():
        for starting_point in starting_points:
            res = []
            x, y = starting_point
            while x >= 0 and x < len(words[0]) and y >= 0 and y < len(words):
                res.append(words[y][x])
                x += dx
                y += dy
            yield "".join(res)
            yield "".join(res[::-1])


def find_pattern(words: list[str]):
    patterns = [
        ["M.M", ".A.", "S.S"],
        ["S.M", ".A.", "S.M"],
        ["S.S", ".A.", "M.M"],
        ["M.S", ".A.", "M.S"],
    ]

    def check(x: int, y: int, pattern: list[str]) -> bool:
        try:
            for dy, line in enumerate(pattern):
                for dx, c in enumerate(line):
                    if c != "." and c != words[y + dy][x + dx]:
                        return False
        except IndexError:
            return False
        return True

    found = 0
    for y in range(len(words)):
        for x in range(len(words[0])):
            for pattern in patterns:
                found += check(x, y, pattern)
    return found


def main():
    words = read_words()
    logger.info("Res a %s", sum(get_count(line) for line in generate_lines(words)))
    logger.info("Res b %s", find_pattern(words))


if __name__ == "__main__":
    init_logging()
    main()
