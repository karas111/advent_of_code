import logging
import os
from bisect import bisect_left
from functools import cmp_to_key
from itertools import chain
from typing import Union

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_packets() -> list[tuple[list, list]]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.readlines()
        for idx in range(0, len(lines), 3):
            res.append((eval(lines[idx]), eval(lines[idx + 1])))
    return res


def int_comp(a: int, b: int) -> int:
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1


def compare_l(a: Union[int, list], b: Union[int, list]) -> int:
    if isinstance(a, int):
        if isinstance(b, int):
            return int_comp(a, b)
        return compare_l([a], b)
    elif isinstance(b, list):
        for a_elem, b_elem in zip(a, b):
            elem_res = compare_l(a_elem, b_elem)
            if elem_res != 0:
                return elem_res
        return int_comp(len(a), len(b))
    else:  # a is list and b is int
        return -compare_l(b, a)


def main():
    packets = read_packets()
    res = [idx + 1 for idx, (a, b) in enumerate(packets) if compare_l(a, b) <= 0]
    logger.info("Result a %s", sum(res))
    raw_packets = list(chain.from_iterable(packets))
    key_func = cmp_to_key(compare_l)
    raw_packets.sort(key=key_func)
    l_idx = bisect_left(raw_packets, key_func([[2]]), key=key_func)
    r_idx = bisect_left(raw_packets, key_func([[6]]), key=key_func)
    # ordering from 1, and not real "insertion"
    logger.info("Res b %s", (l_idx + 1) * (r_idx + 2))


if __name__ == "__main__":
    init_logging()
    main()
