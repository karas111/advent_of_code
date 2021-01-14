import logging
import os
import time
from functools import reduce

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input(part_b=False):
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        if part_b:
            return [ord(x) for x in f.readline().strip()] + [17, 31, 73, 47, 23]
        else:
            return [int(x) for x in f.readline().strip().split(",")]


def one_round_hash(lengths, buffer=None, current_pos=0, skip_size=0):
    if buffer is None:
        buffer = list(range(256))
    buff_len = len(buffer)
    for length in lengths:
        for i in range(length // 2):
            start_idx, end_idx = (current_pos + i) % buff_len, (
                current_pos + length - i - 1
            ) % buff_len
            buffer[start_idx], buffer[end_idx] = buffer[end_idx], buffer[start_idx]
        current_pos += length + skip_size
        skip_size += 1
    return buffer, current_pos, skip_size


def dense_hash(sparse_hash):
    blocks = [sparse_hash[i * 16 : (i + 1) * 16] for i in range(16)]
    return [reduce(lambda x, y: x ^ y, block) for block in blocks]


def hex_repr(hash):
    hex_digits = ["%0.2x" % x for x in hash]
    return "".join(hex_digits)


def knot_hash(lengths):
    buffer = list(range(256))
    current_pos, skip_size = 0, 0
    for _ in range(64):
        buffer, current_pos, skip_size = one_round_hash(
            lengths, buffer, current_pos, skip_size
        )
    dense_h = dense_hash(buffer)
    return hex_repr(dense_h)


def knot_hash_str(stream):
    stream = [ord(x) for x in stream] + [17, 31, 73, 47, 23]
    return knot_hash(stream)


def main():
    lengths = parse_input()
    buffer, _, _ = one_round_hash(lengths)
    # lengths = [3, 4, 1, 5]
    # buffer = one_round_hash(lengths, list(range(5)))
    logger.info(f"Res A {buffer[0] * buffer[1]}")
    lengths = parse_input(part_b=True)
    res_b = knot_hash(lengths)
    logger.info(f"Res B {res_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
