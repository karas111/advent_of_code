import logging
import time
from functools import lru_cache
from collections import deque
import hashlib
import re
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


@lru_cache(maxsize=2000)
def hash_md5(seed, i, part_b):
    passphrase = f"{seed}{i}"
    digest = hashlib.md5(passphrase.encode()).hexdigest()
    if not part_b:
        return digest
    for _ in range(2016):
        digest = hashlib.md5(digest.encode()).hexdigest()
    return digest


@lru_cache(maxsize=10**6)
def has_same_char(word, qty, c=None):
    if c is None:
        c = "."
    pattern_match = re.search("(" + c + r")\1{" + str(qty-1) + r",}", word)
    if pattern_match:
        return pattern_match.groups()[0]
    return None


def is_key(seed, i, part_b):
    digest = hash_md5(seed, i, part_b)
    c = has_same_char(digest, 3)
    if c is None:
        return False
    for j in range(i+1, i+1001):
        digest2 = hash_md5(seed, j, part_b)
        new_c = has_same_char(digest2, 5, c)
        if new_c:
            return True
    return False


def generate_keys(seed, part_b):
    res = []
    i = 0
    while len(res) < 64:
        if is_key(seed, i, part_b):
            res.append(i)
        i += 1
    return res


def main():
    seed = "ihaygndm"
    # seed = "abc"
    res_a = generate_keys(seed, True)
    logger.info(f"Res A {res_a[-1]}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
