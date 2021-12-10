import logging
import os
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

CLOSING = ")]}>"
OPENING = "([{<"
BRACKETS = dict(zip(OPENING, CLOSING))


def read_input() -> List[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


def find_corrupted(line: str, return_incomplete=False):
    stack = []
    for c in line:
        if c in OPENING:
            stack.append(c)
        elif c in CLOSING:
            if stack and c == BRACKETS[stack[-1]]:
                stack.pop()
            else:
                return c, None
        else:
            raise ValueError(f"Wrong character in line {c}")
    return None, stack


def score_corrupted(lines: List[str]) -> int:
    corrupted = [find_corrupted(line)[0] for line in lines]
    corrupted = [x for x in corrupted if x is not None]
    score_value = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(corrupted.count(k) * score for k, score in score_value.items())


def score_autocomplete(lines: List[str]) -> int:
    to_complete = [find_corrupted(line) for line in lines]
    to_complete = [stack for c, stack in to_complete if c is None]
    score_value = {"(": 1, "[": 2, "{": 3, "<": 4}
    line_scores = []
    for line in to_complete:
        line_score = 0
        for c in reversed(line):
            line_score *= 5
            line_score += score_value[c]
        line_scores.append(line_score)
    logger.info(line_scores)
    return sorted(line_scores)[len(line_scores) // 2]


def main():
    lines = read_input()
    logger.info(f"Res a {score_corrupted(lines)}")
    logger.info(f"Res b {score_autocomplete(lines)}")


if __name__ == "__main__":
    init_logging()
    main()
