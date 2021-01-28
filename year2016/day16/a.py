import logging
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def generate_dragon_curve(seed, disk_length):
    a = seed
    while len(a) < disk_length:
        b = "".join(x == "0" and "1" or "0" for x in reversed(a))
        a += "0" + b
    return a[:disk_length]


def get_checksum(data):
    while len(data) % 2 == 0:
        new_data = ""
        for x, y in zip(data[::2], data[1::2]):
            new_data += x == y and "1" or "0"
        data = new_data
    return data


def main():
    seed = "11101000110010100"
    disk_length = 272
    # seed = "10000"
    # disk_length = 20
    data = generate_dragon_curve(seed, disk_length)
    checksum = get_checksum(data)
    logger.info(f"Res A {checksum}")
    disk_length = 35651584
    data = generate_dragon_curve(seed, disk_length)
    checksum = get_checksum(data)
    logger.info(f"Res B {checksum}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
