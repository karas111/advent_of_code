import logging
import os
import re

from z3 import Int, Solver

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[tuple[tuple, tuple]]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(
            r"\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*@\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*"
        )
        for line in f:
            p_l = tuple(map(int, pattern.match(line.strip()).groups()))
            res.append((p_l[:3], p_l[3:]))
        return res


def solve(storms):
    bounadaries = (
        (200000000000000, 400000000000000) if INPUT_FILE == "input.txt" else (7, 27)
    )
    res = 0

    def intersection(storm1, storm2):
        (cords1, vel1), (cords2, vel2) = storm1, storm2
        x1, y1 = cords1[:2]
        x2, y2 = x1 + vel1[0], y1 + vel1[1]
        x3, y3 = cords2[:2]
        x4, y4 = x3 + vel2[0], y3 + vel2[1]
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        num_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        num_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

        px = num_x / denom
        py = num_y / denom
        return (px, py)

    for idx1, storm1 in enumerate(storms[:-1]):
        for storm2 in storms[idx1 + 1 :]:
            p = intersection(storm1, storm2)
            if p is None:
                continue
            if (p[0] - storm1[0][0]) / storm1[1][0] < 0:
                continue
            if (p[0] - storm2[0][0]) / storm2[1][0] < 0:
                continue
            if (
                p[0] < bounadaries[0]
                or p[0] > bounadaries[1]
                or p[1] < bounadaries[0]
                or p[1] > bounadaries[1]
            ):
                continue

            res += 1
    return res


def solve_b(storms):
    x, y, z, dx, dy, dz = [Int(c) for c in "x,y,z,dx,dy,dz".split(",")]
    s = Solver()
    for t_idx, ((sx, sy, sz), (svx, svy, svz)) in enumerate(storms):
        t = Int(f"t{t_idx}")
        s.add(
            x + dx * t == sx + svx * t,
            y + dy * t == sy + svy * t,
            z + dz * t == sz + svz * t,
            t > 0,
        )
    s.check()
    m = s.model()
    return [m[x].as_long(), m[y].as_long(), m[z].as_long()]


def main():
    storms = read_input()
    res = solve(storms)
    logger.info("Res a: %d", res)
    res = solve_b(storms)
    logger.info("Res b: %s", sum(res))


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
