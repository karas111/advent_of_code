import logging
import os
import re
from typing import NamedTuple

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_blueprints() -> list[list[tuple]]:
    blueprints = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = r"Blueprint .*: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
        for line in f:
            res = list(map(int, re.match(pattern, line).groups()))
            robots = [
                tuple([res[0], 0, 0, 0]),
                tuple([res[1], 0, 0, 0]),
                tuple([res[2], res[3], 0, 0]),
                tuple([res[4], 0, res[5], 0]),
            ]
            blueprints.append(robots)
    return blueprints


class State(NamedTuple):
    resources: tuple
    robots: tuple


def compare_all_lt(t1: tuple, t2: tuple) -> bool:
    return all(a < b for a, b in zip(t1, t2))


def find_best(blueprint: list[tuple], time_: int):
    starting_state = State(tuple([0, 0, 0, 0]), tuple([1, 0, 0, 0]))
    max_robots = [max(r_q[i] for r_q in blueprint) for i in range(3)]
    max_robots.append(float("inf"))

    states = {starting_state}
    all_states = {starting_state}
    for time_elapsed in range(time_):
        time_remaining = time_ - time_elapsed
        current_max_production = max(
            state.resources[3] + state.robots[3] * (time_ - time_elapsed)
            for state in states
        )
        new_states = set()

        for state in states:
            robots_to_build = [None]  # encodes not building
            for robot in range(3, -1, -1):
                robot_req = blueprint[robot]
                if max_robots[robot] > state.robots[robot] and all(
                    a <= b for a, b in zip(robot_req, state.resources)
                ):
                    robots_to_build.append(robot)

            # if geode robot can be build, do it
            if 3 in robots_to_build:
                robots_to_build = [3]

            # if all the reobots can be build then remove "do nothing"
            if len(robots_to_build) == 5:
                robots_to_build = robots_to_build[1:]

            # do not produce any robots if that's the last second
            if time_ - time_elapsed <= 1:
                robots_to_build = [None]

            new_resources = tuple(a + b for a, b in zip(state.resources, state.robots))
            for robot in robots_to_build:
                if robot is None:
                    new_robots = state.robots
                    resources = new_resources
                else:
                    resources = tuple(
                        a - b for a, b in zip(new_resources, blueprint[robot])
                    )
                    new_robots = tuple(state.robots[i] + (i == robot) for i in range(4))
                state_ = State(resources, new_robots)
                max_pot_production = (
                    state_.resources[3]
                    + state_.robots[3] * time_remaining
                    + time_remaining * (time_remaining - 1) // 2
                )
                if (
                    max_pot_production >= current_max_production
                    and state_ not in all_states
                ):
                    new_states.add(state_)
                    all_states.add(state_)
        logger.info(
            "After %d time, looking at %d states.", time_elapsed + 1, len(new_states)
        )
        states = new_states

    return max(state.resources[3] for state in states)


def main():
    blueprints = read_blueprints()
    res = [(i + 1) * find_best(b, time_=24) for i, b in enumerate(blueprints)]
    logger.info("Result a %s", sum(res))

    # res = [find_best(b, time_=32) for b in blueprints[:3]]
    # logger.info("Result b %s", res[0] * res[1] * res[2])


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
