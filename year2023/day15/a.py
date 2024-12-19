import logging
import os
from collections import OrderedDict
from functools import reduce

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip().split(",")


def hash_me(word: str) -> int:

    def _hash(seed: int, c: str) -> int:
        res = ((seed + ord(c)) * 17) & ((1 << 8) - 1)
        return res

    return reduce(_hash, word, 0)


def hashmap(words: list[str]) -> int:
    boxes = [OrderedDict() for _ in range(256)]
    for word in words:
        if "=" in word:
            label, focal_s = word.split("=")
            focal_s = int(focal_s)
            box = boxes[hash_me(label)]
            box[label] = focal_s
        else:  # "-"
            label = word[:-1]
            box = boxes[hash_me(label)]
            if label in box:
                del box[label]

    res = 0
    for box_id, box in enumerate(boxes):
        for lens_id, focal_s in enumerate(box.values()):
            res += (box_id + 1) * (lens_id + 1) * focal_s
    return res


def main():
    words = read_input()
    with catchtime(logger):
        hashes = list(map(hash_me, words))
        logger.info("Res A: %s", sum(hashes))
        logger.info("Res B: %s", hashmap(words))


if __name__ == "__main__":
    init_logging()
    main()
