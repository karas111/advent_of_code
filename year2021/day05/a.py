import logging
import os
from typing import DefaultDict, List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def gcd(a, b):
    a, b = abs(a), abs(b)
    if a == 0 and b == 0:
        return 1
    elif a < b:
        return gcd(b, a)
    elif b == 0:
        return a
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


class Line:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def is_ver_hor(self):
        return self.start[0] == self.end[0] or self.start[1] == self.end[1]

    def vec_step(self):
        dx, dy = self.end[0] - self.start[0], self.end[1] - self.start[1]
        gcd_vec = gcd(dx, dy)
        return dx // gcd_vec, dy // gcd_vec

    def get_points(self):
        curr = self.start
        vec_step = self.vec_step()
        while curr != self.end:
            yield curr
            curr = curr[0] + vec_step[0], curr[1] + vec_step[1]
        yield curr


def read_input() -> List[Line]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        res = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            start, end = line.split(" -> ")
            start = tuple(int(x.strip()) for x in start.split(","))
            end = tuple(int(x.strip()) for x in end.split(","))
            res.append(Line(start, end))
    return res


def count_points(lines: List[Line], only_hor_ver: bool) -> int:
    visited = DefaultDict(lambda: 0)
    for line in lines:
        if not only_hor_ver or line.is_ver_hor():
            for point in line.get_points():
                visited[point] += 1
    return len([v for v in visited.values() if v > 1])


def main():
    lines = read_input()
    res = count_points(lines, only_hor_ver=True)
    logger.info(f"Result a {res}")
    res = count_points(lines, only_hor_ver=False)
    logger.info(f"Result b {res}")


if __name__ == "__main__":
    init_logging()
    main()
