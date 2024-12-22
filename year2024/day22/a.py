import logging
import os
from collections import defaultdict

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MOD_N = 1 << 24


def read_input() -> list[int]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return list(map(int, f.readlines()))


def hash_me(n: int, n_iter: int = 1) -> list[int]:
    res = [n]
    for _ in range(n_iter):
        n = (n ^ (n << 6)) & (MOD_N - 1)  # * 64
        n = (n ^ (n >> 5)) & (MOD_N - 1)
        n = (n ^ (n << 11)) & (MOD_N - 1)  # * 64
        res.append(n)
    return res


def get_first_seq_occurences(diff_seq):
    res = {}
    for i in range(len(diff_seq) - 4):
        seq = tuple(diff_seq[i : i + 4])
        if seq not in res:
            res[seq] = i
    return res


def solve2(seqs: list[list[int]]):
    prices = [[x % 10 for x in seq] for seq in seqs]
    diffs = [[x1 - x0 for x0, x1 in zip(seq, seq[1:])] for seq in prices]
    diffs = [get_first_seq_occurences(diff_seq) for diff_seq in diffs]
    res = defaultdict(int)
    for price_seq, diff_occ in zip(prices, diffs):
        for sell_inst, idx in diff_occ.items():
            res[sell_inst] += price_seq[idx + 4]
    return max(res.values())


def main():
    ns = read_input()
    with catchtime(logger):
        res = [hash_me(n, n_iter=2000) for n in ns]
        logger.info("Res A: %s", sum([x[-1] for x in res]))
        seqs = [hash_me(n, n_iter=2000) for n in ns]
        res = solve2(seqs)
        logger.info("Res B: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
