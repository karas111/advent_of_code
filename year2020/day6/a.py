import logging
import os
import re
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        data = f.read().strip()
    groups = data.split("\n\n")
    return [group.split("\n") for group in groups]


def count_common_or(groups):
    res = []
    for group in groups:
        group_common = set()
        for person in group:
            group_common = group_common | set(person)
        res.append(group_common)
    return res


def count_common_and(groups):
    res = []
    for group in groups:
        group_common = set(group[0])
        for person in group[1:]:
            group_common = group_common & set(person)
        res.append(group_common)
    return res


def main():
    groups = parse_input()
    group_ans = count_common_or(groups)
    ans_sum = [len(group) for group in group_ans]
    logger.info(f"Ans A {ans_sum}, sum = {sum(ans_sum)}")
    group_ans = count_common_and(groups)
    ans_sum = [len(group) for group in group_ans]
    logger.info(f"Ans B {ans_sum}, sum = {sum(ans_sum)}")

if __name__ == "__main__":
    init_logging()
    main()
