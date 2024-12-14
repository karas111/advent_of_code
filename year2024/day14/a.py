import logging
import math
import os
import re
from collections import defaultdict
from dataclasses import dataclass

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

if INPUT_FILE == "test1.txt":
    MAX_C = 11, 7
else:
    MAX_C = 101, 103


@dataclass
class Robot:
    cords: tuple[int, int]
    vel: tuple[int, int]


def read_input() -> list[Robot]:
    pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            ns = tuple(map(int, re.match(pattern, line).groups()))
            res.append(Robot(cords=ns[:2], vel=ns[2:]))
    return res


def move(robots: list[Robot], niter: int) -> list[Robot]:
    for robot in robots:
        robot.cords = tuple(
            (robot.cords[i] + niter * robot.vel[i]) % MAX_C[i] for i in range(2)
        )
    return robots


def count_score(robots: list[Robot]) -> int:
    res = defaultdict(lambda: 0)
    middle_x, middle_y = tuple(c // 2 for c in MAX_C)
    for robot in robots:
        x, y = robot.cords
        if x == middle_x or y == middle_y:
            continue
        res[((x < middle_x), (y < middle_y))] += 1
    return math.prod(x for x in res.values())


def robots_to_str(robots: list[Robot]) -> str:
    res = [["."] * MAX_C[0] for _ in range(MAX_C[1])]
    robot_set = set()
    for robot in robots:
        res[robot.cords[1]][robot.cords[0]] = "#"
        robot_set.add(robot.cords)

    if len(robot_set) < len(robots):
        return None

    return "\n".join("".join(line) for line in res)


def main():
    robots = read_input()
    with catchtime(logger):
        move(robots, niter=100)
        logger.info("Res A %s", count_score(robots))

    robots = read_input()
    logger.info("After 0 iters\n")
    logger.info(robots_to_str(robots))
    logger.info("\n\n")
    i = 0
    with catchtime(logger):
        while True:
            i += 1
            robots = move(robots, niter=1)
            robot_str = robots_to_str(robots)
            if robot_str or i % 10000 == 0:
                logger.info("Res B:  %s", i)
                logger.info("\n%s", robot_str)
                logger.info("\n")
                break


if __name__ == "__main__":
    init_logging()
    main()
