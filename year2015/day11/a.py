import logging

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

INVALID_LETTERS = "iol"


def has_two_overlapping_pairs(password: str) -> bool:
    pairs = set()
    i = 0
    while i < len(password) - 1:
        if password[i] == password[i + 1]:
            pairs.add(password[i])
            i += 2
        else:
            i += 1
        if len(pairs) >= 2:
            return True
    return False


def has_3_sequence(password: str) -> bool:
    for a, b, c in zip(password, password[1:], password[2:]):
        if ord(a) == ord(b) - 1 and ord(b) == ord(c) - 1:
            return True
    return False


def find_next(password: str) -> str:

    def get_next_string(password: str) -> str:
        chars = list(password)

        i = len(chars) - 1
        while i >= 0:
            chars[i] = chr(ord(chars[i]) + 1)

            if chars[i] in INVALID_LETTERS:
                chars[i] = chr(ord(chars[i]) + 1)

            if chars[i] > "z":
                chars[i] = "a"
                i -= 1
                continue
            for j in range(i + 1, len(chars)):
                chars[j] = "a"
            return "".join(chars)

    while True:
        password = get_next_string(password)
        if has_3_sequence(password) and has_two_overlapping_pairs(password):
            return password


def main():
    password = "hepxcrrq"
    new_password = find_next(password)
    logger.info("Res a: %s", new_password)
    new_password = find_next(new_password)
    logger.info("Res b: %s", new_password)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
