import logging
import os
import time
import re
from collections import deque
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line]


def scramble(seed, instructions, reverse=False):
    swap_pos = r"swap position (\d+) with position (\d+)"
    swap_letters = r"swap letter (.+) with letter (.+)"
    rotate = r"rotate (left|right) (\d+) step(.)?"
    rotate_based_pos = r"rotate based on position of letter (.+)"
    reverse_pattern = r"reverse positions (\d+) through (\d+)"
    move = r"move position (\d+) to position (\d+)"
    password = deque(seed)
    if reverse:
        instructions = reversed(instructions)
    for inst in instructions:
        if (match := re.match(swap_pos, inst)):
            x, y = [int(arg) for arg in match.groups()]
            password[x], password[y] = password[y], password[x]
        elif (match := re.match(swap_letters, inst)):
            a, b = match.groups()
            x, y = password.index(a), password.index(b)
            password[x], password[y] = password[y], password[x]
        elif (match := re.match(rotate, inst)):
            left_right, pos, *args = match.groups()
            pos = int(pos) * (left_right == "left" and -1 or 1)
            pos *= reverse and -1 or 1
            password.rotate(pos)
        elif (match := re.match(rotate_based_pos, inst)):
            idx = password.index(match.groups()[0])
            if reverse:
                new_old_pos = {1: 0, 3: 1, 5: 2, 7: 3, 2: 4, 4: 5, 6: 6, 0: 7}
                idx = new_old_pos[idx]
                pos = -(1 + idx + (idx >= 4 and 1 or 0))
            else:
                pos = 1 + idx + (idx >= 4 and 1 or 0)
            password.rotate(pos)
        elif (match := re.match(reverse_pattern, inst)):
            x, y = [int(arg) for arg in match.groups()]
            password_lst = list(password)
            password_lst[x:y+1] = reversed(password_lst[x:y+1])
            password = deque(password_lst)
        elif (match := re.match(move, inst)):
            x, y = [int(arg) for arg in match.groups()]
            if reverse:
                x, y = y, x
            a = password[x]
            password.remove(a)
            password.insert(y, a)
        else:
            raise ValueError("No match")
    return "".join(password)


def main():
    instructions = parse_input()
    seed = "abcdefgh"
    passphrase = scramble(seed, instructions)
    logger.info(f"Res A {passphrase}")
    passphrase = "fbgdceah"
    seed = scramble(passphrase, instructions, reverse=True)
    logger.info(f"Res B {seed}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
