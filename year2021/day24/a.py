import logging
import os
import re
from pprint import pformat
from typing import NamedTuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Params(NamedTuple):
    a: int
    b: int
    c: int


def read_input() -> list[Params]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = [line.strip() for line in f]
    pattern = re.compile(r"-?\d+")
    res = []
    iter_len = 18
    for i in range(14):
        a, b, c = [
            int(re.search(pattern, lines[i * iter_len + offset]).group(0))
            for offset in [4, 5, 15]
        ]
        res.append(Params(int(a == 26), b, c))
    return res


def number_to_str(n):
    if n >= 0:
        return f"+ {n}"
    else:
        return f"- {abs(n)}"


def find_biggest(cond_params: list[tuple[int, int, int]]) -> str:
    res = [-1] * 14
    for low_id, high_id, diff in cond_params:
        if diff < 0:
            res[low_id] = 9
            res[high_id] = 9 + diff
        else:
            res[high_id] = 9
            res[low_id] = 9 - diff
    return "".join([str(x) for x in res])


def find_smallest(cond_params: list[tuple[int, int, int]]) -> str:
    res = [-1] * 14
    for low_id, high_id, diff in cond_params:
        if diff > 0:
            res[low_id] = 1
            res[high_id] = 1 + diff
        else:
            res[high_id] = 1
            res[low_id] = 1 - diff
    return "".join([str(x) for x in res])


def main():
    # x = (z % 26 + b) != w
    # z //= 25 * a + 1
    # if x:
    #     z = 26*z + w + c

    # if a[i] == 1
    # w[i-1] + c[i-1] + b[i] == w[i]
    # w[2] + 1 - 4 == w[2]

    params = read_input()
    logger.info("Input\n%s", pformat(list(enumerate(params))))
    conditions = []
    cond_params = []
    heap = []
    for i in range(len(params)):
        new_param = params[i]
        if params[i].a:
            old_id, old_param = heap.pop()
            conditions.append(
                f"w[{old_id}] {number_to_str(old_param.c + new_param.b)} == w[{i}]"
            )
            cond_params.append((old_id, i, old_param.c + new_param.b))
        else:
            heap.append((i, new_param))
    logger.info("Conditions\n%s", "\n".join(conditions))
    logger.info("Res A: %s", find_biggest(cond_params))
    logger.info("Res B: %s", find_smallest(cond_params))


if __name__ == "__main__":
    init_logging()
    main()
