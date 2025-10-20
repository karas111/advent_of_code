import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_ranges() -> list[tuple[range, range]]:
    def parse_line(line: str) -> tuple[range, range]:
        res = []
        for range_ in line.strip().split(","):
            a, b = map(int, range_.split("-"))
            res.append(range(a, b + 1))
        return res

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return list(map(parse_line, f.readlines()))


def is_included(a: range, b: range) -> bool:
    if a.start > b.start:
        a, b = b, a
    return a.start == b.start or a.stop >= b.stop


def is_intersect(a: range, b: range) -> bool:
    if a.start > b.start:
        a, b = b, a
    return a.start == b.start or a.stop > b.start


def main():
    ranges = read_ranges()
    res = [is_included(a, b) for a, b in ranges]
    logger.info("Result a %d", sum(res))
    res = [is_intersect(a, b) for a, b in ranges]
    logger.info("Result b %d", sum(res))


if __name__ == "__main__":
    init_logging()
    main()
