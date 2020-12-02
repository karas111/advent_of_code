import logging
import os
from collections import namedtuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Policy = namedtuple("Policy", ["min", "max", "char"])
Entry = namedtuple("Entry", ["policy", "password"])


def read_input():
    def parse_line(line):
        policy, password = line.split(": ")
        minmax, char = policy.split(" ")
        min_c, max_c = minmax.split("-")
        return Entry(Policy(int(min_c), int(max_c), char), password)

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_line(line) for line in f if line]


def is_valida(entry):
    res = {}
    for c in entry.password:
        res[c] = res.get(c, 0) + 1
    return entry.policy.min <= res.get(entry.policy.char, 0) <= entry.policy.max


def is_validb(entry):
    pol = entry.policy
    return (entry.password[pol.min - 1] == pol.char) != (
        entry.password[pol.max - 1] == pol.char
    )


def main():
    entries = read_input()
    valid_passwords = [is_valida(entry) for entry in entries]
    # logger.info(f"Valind passwords {valid_passwords}")
    logger.info(f"Valid A passwords {sum(valid_passwords)}")
    valid_passwords = [is_validb(entry) for entry in entries]
    # logger.info(f"Valid B passwords {valid_passwords}")
    logger.info(f"Valid B passwords {sum(valid_passwords)}")


if __name__ == "__main__":
    init_logging()
    main()
