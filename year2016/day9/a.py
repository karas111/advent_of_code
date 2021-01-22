import logging
import os
import re
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return f.readline().strip()


def get_dec_len(line, rec=False):
    ptr = 0
    dec_len = 0
    while ptr < len(line):
        c = line[ptr]
        if c == "(":
            close_ptr = line[ptr:].index(")") + ptr
            patt_len, times = [
                int(x)
                for x in re.match(
                    r"\((\d+)x(\d+)\)", line[ptr: close_ptr + 1]
                ).groups()
            ]
            pattern = line[close_ptr + 1: close_ptr + 1 + patt_len]
            if rec:
                new_patt_len = get_dec_len(pattern, rec=True)
                dec_len += new_patt_len * times
            else:
                dec_len += patt_len * times
            ptr = close_ptr + 1 + patt_len
        else:
            dec_len += 1
            ptr += 1
    return dec_len


def main():
    line = parse_input()
    # line = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
    res_a = get_dec_len(line)
    logger.info(f"Res A {res_a}")
    res_b = get_dec_len(line, rec=True)
    logger.info(f"Res A {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
