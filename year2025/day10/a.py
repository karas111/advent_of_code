import logging
import os
import re
from typing import NamedTuple

from pyparsing import deque
from z3 import Int, Optimize

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class State(NamedTuple):
    lights: int
    edges: list[list[int]]
    joltage: list[int]


def read_input():
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            lights = re.search(r"\[(.*?)\]", line).group(1)
            lights = lights.replace(".", "0").replace("#", "1")
            lights = int(lights[::-1], base=2)

            paren_items = re.findall(r"\((.*?)\)", line)

            edges = []
            for item in paren_items:
                edges.append(tuple(map(int, item.split(","))))

            joltage = re.search(r"\{(.*?)\}", line)
            joltage = list(map(int, joltage.group(1).split(",")))

            res.append(State(lights, edges, joltage))
    return res


def solve(states: list[State], part_b=False) -> int:

    def solve_state_a(state: State) -> int:
        queue = deque([(0, 0)])
        distances = {}
        while queue:
            lights, dist = queue.popleft()
            if lights in distances:
                continue
            distances[lights] = dist
            if lights == state.lights:
                return distances[lights]
            for switch in state.edges:
                next_lights = lights
                for n_bit in switch:
                    # toggle bit
                    next_lights = next_lights ^ (1 << n_bit)
                queue.append((next_lights, dist + 1))
        return

    def solve_state_b(state: State):
        presses = [Int(f"x{i}") for i in range(len(state.edges))]

        opt = Optimize()
        for x in presses:
            opt.add(x >= 0)
        for idx, jolt in enumerate(state.joltage):
            jolt_req = sum(
                presses[e_idx] for e_idx, edge in enumerate(state.edges) if idx in edge
            )
            opt.add(jolt_req == jolt)

        x_sum = sum(presses)
        h = opt.minimize(x_sum)
        opt.check()
        opt.lower(h)
        mdl = opt.model()
        return mdl.evaluate(x_sum).as_long()

    if part_b:
        return [solve_state_b(state) for state in states]
    return [solve_state_a(state) for state in states]


def main():
    states = read_input()
    res = solve(states)
    logger.info("Result a %s", sum(res))
    res = solve(states, part_b=True)
    logger.info("Result b %s", sum(res))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
