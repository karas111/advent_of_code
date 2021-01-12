import logging
import os
import time
from collections import Counter
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip().split(" ") for line in f.readlines() if line]


def is_valid_b(passphrase: List[str]) -> bool:
    used_words = set()
    for word in passphrase:
        arrity = tuple(sorted(Counter(word).items()))
        if arrity in used_words:
            return False
        used_words.add(arrity)
    return True


def is_valid_a(passphrase: List[str]) -> bool:
    used_words = set()
    for word in passphrase:
        if word in used_words:
            return False
        used_words.add(word)
    return True


def main():
    passphrases = parse_input()
    valid = [passphrase for passphrase in passphrases if is_valid_a(passphrase)]
    logger.info(f"Res A {len(valid)}")
    valid = [passphrase for passphrase in passphrases if is_valid_b(passphrase)]
    logger.info(f"Res B {len(valid)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
