import logging
import os
from typing import List, NamedTuple, Tuple, Set

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Point = Tuple[int, int]


class Instruction(NamedTuple):
    horizontal: bool
    axis: int


def read_input() -> Tuple[List[Point], List[Instruction]]:
    points, instructions = [], []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        points_str, instructions_str = f.read().split("\n\n", maxsplit=1)
        points = [
            tuple(int(x) for x in point_line.strip().split(","))
            for point_line in points_str.split("\n")
            if point_line.strip()
        ]
        fold_prefix = "fold along "
        instructions = [
            Instruction(
                horizontal=fold_line[len(fold_prefix)] == "x",
                axis=int(fold_line.strip()[len(fold_prefix) + 2:]),
            )
            for fold_line in instructions_str.split("\n")
            if fold_line.startswith(fold_prefix)
        ]

    return points, instructions


def do_fold(points: List[Point], folds: List[Instruction]) -> Set[Tuple[int, int]]:
    res = set()
    for x, y in points:
        for fold in folds:
            if fold.horizontal and x > fold.axis:
                x = 2 * fold.axis - x
            if not fold.horizontal and y > fold.axis:
                y = 2 * fold.axis - y
        res.add((x, y))
    return res


def display_points(final_points: Set[Point]) -> str:
    max_x = max(x[0] for x in final_points)
    min_x = min(x[0] for x in final_points)
    max_y = max(x[1] for x in final_points)
    min_y = min(x[1] for x in final_points)
    res = []
    for y in range(min_y, max_y + 1):
        res.append(
            "".join(
                "#" if (x, y) in final_points else "." for x in range(min_x, max_x + 1)
            )
        )
    return "\n".join(res)


def main():
    points, instructions = read_input()
    logger.info(f"Res a {len(do_fold(points, instructions[:1]))}")
    final_points = do_fold(points, instructions)
    res = display_points(final_points)
    logger.info(f"Res b:\n\n{res}")


if __name__ == "__main__":
    init_logging()
    main()
