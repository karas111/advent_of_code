from functools import cached_property, lru_cache
import logging
import os
import re
import time
import copy
from collections import namedtuple
from typing import Pattern

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Rule:
    def __init__(self, pattern, out_img) -> None:
        self.pattern = pattern
        self.out_img = out_img

    @cached_property
    def all_patterns(self):
        res = []
        for k in range(4):
            pattern = np.rot90(self.pattern, k=k)
            res.append(pattern)
            res.append(np.flip(pattern, axis=0))
        return res

    @lru_cache(maxsize=None)
    def is_matching(self, img):
        img = np.array(img)
        return self.pattern.shape == img.shape and any(np.all(pattern == img) for pattern in self.all_patterns)


def parse_input():
    def parse_coding(pattern):
        return np.array([[x == "#" for x in line] for line in pattern.split("/")])

    def parse_rule(line):
        pattern, out_img = re.match("(.*) => (.*)", line).groups()
        return Rule(parse_coding(pattern), parse_coding(out_img))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_rule(line.strip()) for line in f.readlines() if line]


def paint(img, rules, iterations=5):
    def apply_rules(sub_img):
        for rule in rules:
            if rule.is_matching(tuple(tuple(x) for x in sub_img)):
                return copy.copy(rule.out_img)
        raise ValueError("No matching rule")

    for i in range(iterations):
        logger.info(f"Start iteration {i}")
        size = img.shape[0]
        grid_size = size // 2 if size % 2 == 0 else size // 3
        assert size % grid_size == 0
        grid = [np.hsplit(y, grid_size) for y in np.vsplit(img, grid_size)]
        grid = [[apply_rules(block) for block in block_line] for block_line in grid]
        img = np.concatenate([np.concatenate(line, axis=1) for line in grid])
        print(img)
        logger.info(f"End {i}. Shape {img.shape}. Pixels {np.sum(img)}")
    return img


def main():
    rules = parse_input()
    starting_img = np.array([[False, True, False], [False, False, True], [True, True, True]])
    img = paint(starting_img, rules, 18)
    logger.info(f"Res A {np.sum(img)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
