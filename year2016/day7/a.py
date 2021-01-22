import logging
import os
import re
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f.readlines() if line]


def get_ip7(line):
    addresses = re.split(r"\[([a-z]*)\]", line)
    return addresses[::2], addresses[1::2]


def is_abba(word):
    return any(
        a == d and b == c and a != b
        for a, b, c, d in zip(word, word[1:], word[2:], word[3:])
    )


def is_tls(address):
    return any(is_abba(word) for word in address[0]) and not any(
        is_abba(word) for word in address[1]
    )


def get_abas(word):
    res = []
    for a, b, c in zip(word, word[1:], word[2:]):
        if a == c and a != b:
            res.append(a + b + c)
    return res


def is_ssl(address):
    abas = sum([get_abas(word) for word in address[0]], [])
    for aba in abas:
        bab = aba[1] + aba[0] + aba[1]
        if any(bab in word for word in address[1]):
            return True
    return False


def main():
    lines = parse_input()
    addresses = [get_ip7(line) for line in lines]
    addresses_tls = [a for a in addresses if is_tls(a)]
    addresses_ssl = [a for a in addresses if is_ssl(a)]
    logger.info(f"Res A {len(addresses_tls)}")
    logger.info(f"Res B {len(addresses_ssl)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
