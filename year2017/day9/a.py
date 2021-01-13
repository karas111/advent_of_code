import logging
import os
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def get_group_score(stream) -> int:
    tot_score = 0
    tot_garbage = 0
    groups = 0
    in_garbage = False
    cancel_next = False
    for c in stream:
        if in_garbage:
            if cancel_next:
                cancel_next = False
            elif c == ">":
                in_garbage = False
            elif c == "!":
                cancel_next = True
            else:
                tot_garbage += 1
            continue
        else:
            if c == "<":
                in_garbage = True
                continue
            elif c == "{":
                groups += 1
                tot_score += groups
                continue
            elif c == "}":
                groups -= 1
                continue
            elif c == ",":
                continue
            else:
                raise ValueError(f"Can't process {c}")
    return tot_score, tot_garbage


def main():
    stream = parse_input()
    # stream = "{{<!!>},{<!!>},{<!!>},{<!!>}}"
    logger.info(f"Res A {get_group_score(stream)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
