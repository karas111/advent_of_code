import logging
import os
import re
from functools import cache

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def calculate(lava: str, springs: list[int]) -> int:
    lava = lava + "."

    @cache
    def _calculate(lava_idx: int, spring_idx: int) -> int:
        r = 0
        if lava_idx == len(lava):
            return spring_idx == len(springs)

        if lava[lava_idx] in ".?":
            r += _calculate(lava_idx + 1, spring_idx)

        if spring_idx >= len(springs):
            return r
        lava_end_idx = lava_idx + springs[spring_idx]
        if len(lava) <= lava_end_idx:
            return r
        if "." not in lava[lava_idx:lava_end_idx] and (
            len(lava) == lava_end_idx or lava[lava_end_idx] != "#"
        ):
            r += _calculate(lava_end_idx + 1, spring_idx + 1)
        return r

    return _calculate(0, 0)


def read_input() -> list[tuple[str, list[int]]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(r"([.#?]+) ([\d,]+)")
        res = []
        for line in f:
            img, numbers = re.match(pattern, line).groups()
            res.append((img, list(map(int, numbers.split(",")))))
        return res


def main():
    descs = read_input()
    with catchtime(logger):
        res = [calculate(lava, springs) for lava, springs in descs]
        logger.info("Res A: %s", sum(res))

        res = [
            calculate(((lava + "?") * 5)[:-1], springs * 5) for lava, springs in descs
        ]
        logger.info("Res B: %s", sum(res))


if __name__ == "__main__":
    init_logging()
    main()
