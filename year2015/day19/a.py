import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> tuple[list[tuple[str, str]], str]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        while True:
            line = f.readline().strip()
            if not line:
                return res, f.readline().strip()
            res.append(line.split(" => "))


def apply_rule(word: str, from_: str, to: str) -> set[str]:
    res = set()
    parts = word.split(from_)
    for idx in range(len(parts) - 1):
        new_w = from_.join(parts[: idx + 1]) + to + from_.join(parts[idx + 1 :])
        res.add(new_w)
    return res


def simulate(rules: list[tuple[str, str]], word: str) -> int:
    res = set()
    for from_, to in rules:
        res.update(apply_rule(word, from_, to))
    return len(res)


def solve_b(word: str) -> int:
    return (
        sum(c.isupper() for c in word)
        - word.count("Rn")
        - word.count("Ar")
        - 2 * word.count("Y")
        - 1
    )


def main():
    rules, word = read_input()
    res = simulate(rules, word)
    logger.info("Res a: %s", res)
    res = solve_b(word)
    logger.info("Res b: %s", res)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
