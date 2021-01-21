import logging
import os
import time

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


MOVE_VEC = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}

KEYPAD = {(j, i): str(i * 3 + j + 1) for i in range(3) for j in range(3)}
KEYPAD_B = {
    (0, -2): "1",
    (-1, -1): "2",
    (0, -1): "3",
    (1, -1): "4",
    (-2, 0): "5",
    (-1, 0): "6",
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
    (-1, 1): "A",
    (0, 1): "B",
    (1, 1): "C",
    (0, 2): "D",
}


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line]


def main():
    instructions = parse_input()
    data = [
        (np.array([1, 1]), KEYPAD),
        (np.array([-2, 0]), KEYPAD_B),
    ]
    for pos, keypad in data:
        res = ""
        for inst in instructions:
            for c in inst:
                new_pos = pos + MOVE_VEC[c]
                if tuple(new_pos) in keypad:
                    pos = new_pos
            res += keypad[tuple(pos)]
        logger.info(f"Res {res}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
