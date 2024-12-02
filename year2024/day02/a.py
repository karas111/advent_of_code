import os
import logging
import re
from typing import Iterable

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_reports() -> Iterable[list[int]]:
    pattern = re.compile(r"\b\d+\b")
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            yield [int(x) for x in pattern.findall(line)]


def is_valid(report: list[int]) -> bool:
    sign = None
    for x, y in zip(report, report[1:]):
        if sign is None:
            sign = x > y
        if sign != (x > y):
            return False
        if abs(x - y) > 3 or x == y:
            return False
    return True


def is_valid2(report: list[int]) -> bool:
    return any(is_valid(report[:i] + report[i + 1 :]) for i in range(len(report)))


def count_valid(reports: list[list[int]], part2: bool) -> int:
    if part2:
        return sum(is_valid2(report) for report in reports)
    else:
        return sum(is_valid(report) for report in reports)


def main():
    reports = list(read_reports())
    logger.info(f"Result a {count_valid(reports, part2=False)}")
    logger.info(f"Result b {count_valid(reports, part2=True)}")


if __name__ == "__main__":
    init_logging()
    main()
