import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Grid = list[str]


def convert_to_n(g: Grid) -> tuple[list[int], list[int]]:
    res_x = [int(line, base=2) for line in g]
    res_y = [int("".join(line), base=2) for line in zip(*g)]
    return res_x, res_y


def find_mirror_score(g: Grid, with_smuge: bool = False) -> int:

    def seq_compare(seq1: list[int], seq2: list[int]) -> bool:
        if not with_smuge:
            return seq1[: len(seq2)] == seq2[: len(seq1)]
        # for the second part, there can be only one pair of numbers
        # that differs with exactly one bit
        return sum((x0 ^ x1).bit_count() for x0, x1 in zip(seq1, seq2)) == 1

    def mirror_point(seq: list[int]):
        for i in range(1, len(seq)):
            seq1, seq2 = seq[:i][::-1], seq[i:]
            if seq_compare(seq1, seq2):
                return i
        return 0

    x_seq, y_seq = convert_to_n(g)
    return 100 * mirror_point(x_seq) + mirror_point(y_seq)


def read_input() -> list[Grid]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for g_combined in f.read().split("\n\n"):
            res.append(
                [
                    l.strip().replace("#", "1").replace(".", "0")
                    for l in g_combined.splitlines()
                ]
            )
    return res


def main():
    grids = read_input()
    with catchtime(logger):
        logger.info("Res A: %s", sum(find_mirror_score(grid) for grid in grids))
        logger.info(
            "Res B: %s", sum(find_mirror_score(grid, with_smuge=True) for grid in grids)
        )


if __name__ == "__main__":
    init_logging()
    main()
