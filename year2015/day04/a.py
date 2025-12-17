import logging
import os
from hashlib import md5

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def find_hash(secret, upper_bound=10**7, required_zeroes=5):
    for i in range(upper_bound):
        hash_ = md5(f"{secret}{i}".encode("utf-8")).hexdigest()
        if hash_.startswith("0" * required_zeroes):
            return i


def main():
    secret = read_input()
    logger.info("Res a: %d", find_hash(secret, required_zeroes=5))
    logger.info("Res b: %d", find_hash(secret, required_zeroes=6))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
