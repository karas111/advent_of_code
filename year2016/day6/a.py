import logging
import os
import time
from collections import Counter

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line]


def main():
    words = parse_input()
    letters = [Counter(letters).most_common(1)[0][0] for letters in zip(*words)]
    res_a = "".join(letters)
    logger.info(f"Res A {res_a}")
    letters = [Counter(letters).most_common()[-1][0] for letters in zip(*words)]
    res_b = "".join(letters)
    logger.info(f"Res B {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
