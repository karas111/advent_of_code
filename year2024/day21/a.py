import logging
import os
from collections import Counter

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

NUM_PAD = {c: (i % 3, i // 3) for i, c in enumerate("789456123 0A")}
DIR_PAD = {c: (i % 3, i // 3) for i, c in enumerate(" ^A<v>")}


def read_input() -> list[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [l.strip() for l in f]


def get_needed_steps(
    seq: str, key_pad: dict[str, tuple[int, int]], multiplier: int
) -> Counter[str]:
    res = Counter()
    gap_x, gap_y = key_pad[" "]

    x, y = key_pad["A"]
    for c in seq:
        nx, ny = key_pad[c]
        dx, dy = nx - x, ny - y
        through_gap = (nx == gap_x and y == gap_y) or (x == gap_x and ny == gap_y)
        # priority < v ^ >
        pref_path = "<" * -dx + "v" * dy + "^" * -dy + ">" * dx
        if through_gap:
            pref_path = pref_path[::-1]
        pref_path = pref_path + "A"
        res[pref_path] += multiplier
        x, y = nx, ny
    return res


def solve(codes: list[str], n_iter: int) -> int:
    res = 0
    for code in codes:
        seqs = get_needed_steps(code, NUM_PAD, 1)
        for _ in range(n_iter):
            seqs = sum(
                (
                    get_needed_steps(part, DIR_PAD, count)
                    for part, count in seqs.items()
                ),
                Counter(),
            )
        res += sum(len(k) * v for k, v in seqs.items()) * int(code[:3])
    return res


def main():
    codes = read_input()
    with catchtime(logger):
        res = solve(codes, 2)
        logger.info("Res A: %s", res)
        res = solve(codes, 25)
        logger.info("Res B: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
