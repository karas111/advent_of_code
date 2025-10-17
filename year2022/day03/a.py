import logging
import os
from functools import reduce

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_packages() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [l.strip() for l in f.readlines()]


def score(s: str) -> int:
    if ord(s) <= ord("Z"):
        return 27 + ord(s) - ord("A")
    return 1 + ord(s) - ord("a")


def get_error_score(pkg: str) -> int:
    error = set(pkg[: len(pkg) // 2]).intersection(set(pkg[len(pkg) // 2 :])).pop()
    return score(error)


def get_groups_badge(groups: list[str]) -> int:
    badge = reduce(
        lambda c, l: c.intersection(set(l)), groups[1:], set(groups[0])
    ).pop()
    return score(badge)


def main():
    packages = read_packages()
    errors_scores = map(get_error_score, packages)
    logger.info("Result a %d", sum(errors_scores))

    groups = [packages[i : i + 3] for i in range(0, len(packages), 3)]
    badge_scores = map(get_groups_badge, groups)
    logger.info("Result b %d", sum(badge_scores))


if __name__ == "__main__":
    init_logging()
    main()
