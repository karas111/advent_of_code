import logging
import os
import re
from typing import NamedTuple

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Reindeer(NamedTuple):
    name: str
    speed: int
    speed_time: int
    rest_time: int

    def distance(self, t: int) -> int:
        cycle_time = self.speed_time + self.rest_time
        full_cycles = t // cycle_time
        remaining_time = t % cycle_time
        return (
            full_cycles * self.speed * self.speed_time
            + min(remaining_time, self.speed_time) * self.speed
        )


def read_input() -> list[Reindeer]:
    pattern = r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            name, speed, speed_time, rest_time = re.match(
                pattern, line.strip()
            ).groups()
            res.append(Reindeer(name, int(speed), int(speed_time), int(rest_time)))
    return res


def score_points(reindeers: list[Reindeer], max_t: int) -> list[int]:
    res = [0] * len(reindeers)
    for t in range(1, max_t + 1):
        round_res = [r.distance(t) for r in reindeers]
        max_d = max(round_res)
        for i in range(len(reindeers)):
            if round_res[i] == max_d:
                res[i] += 1
    return res


def main():
    reindeers = read_input()
    t = 2503
    reind_sort = sorted(reindeers, key=lambda r: r.distance(t))
    logger.info("Res a: %d", reind_sort[-1].distance(t))
    res_b = score_points(reindeers, t)
    logger.info("Res a: %d", max(res_b))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
