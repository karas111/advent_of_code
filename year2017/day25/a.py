import logging
import os
import re
import time
from collections import namedtuple
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

State = namedtuple("State", ["inst_0", "inst_1"])
Instruction = namedtuple("Instruction", ["val", "move", "next_state"])


def parse_input():
    def parse_inst(lines):
        val = int(re.match("    - Write the value (0|1).", lines[0]).groups()[0])
        move = re.match("    - Move one slot to the (left|right).", lines[1]).groups()[
            0
        ]
        move = move == "left" and -1 or 1
        next_state = re.match("    - Continue with state (.*).", lines[2]).groups()[0]
        return Instruction(val, move, next_state)

    def parse_state(state_str):
        lines = state_str.split("\n")
        state_name = re.match("In state (.*):", lines[0]).groups()[0]
        inst_0 = parse_inst(lines[2:5])
        inst_1 = parse_inst(lines[6:9])
        return state_name, State(inst_0, inst_1)

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.readlines()
    start_state = re.match("Begin in state (.*).", lines[0]).groups()[0]
    steps = int(
        re.match(
            r"Perform a diagnostic checksum after (\d+) steps.", lines[1]
        ).groups()[0]
    )
    states = "".join(lines[2:]).strip().split("\n\n")
    states = dict(parse_state(state) for state in states)
    return start_state, steps, states


def run(current_state, steps, states):
    tapes = {}
    current_pos = 0
    for _ in range(steps):
        val = tapes.get(current_pos, 0)
        inst = val == 0 and current_state.inst_0 or current_state.inst_1
        tapes[current_pos] = inst.val
        current_pos += inst.move
        current_state = states[inst.next_state]
    return tapes


def main():
    start_state, steps, states = parse_input()
    tapes = run(states[start_state], steps, states)
    logger.info(f"Res A {sum(tapes.values())}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
