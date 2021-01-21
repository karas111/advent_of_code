import logging
import os
import re
import time
from collections import Counter

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Room:
    def __init__(self, name, sector_id, checksum) -> None:
        self.name = name
        self.sector_id = sector_id
        self.checksum = checksum

    @property
    def is_real(self):
        name = self.name.replace("-", "")
        checksum = sorted(Counter(name).items(), key=lambda x: (-x[1], x[0]))
        checksum = "".join([x[0] for x in checksum[:5]])
        return checksum == self.checksum

    @property
    def decrypted_name(self):
        new_name = ""
        tot_alpha_len = ord("z") + 1 - ord("a")
        for c in self.name:
            if c == "-":
                new_name += " "
            else:
                new_name += chr(ord("a") + (ord(c) - ord("a") + self.sector_id) % tot_alpha_len)
        return new_name


def parse_input():
    def parse_room(line):
        name, sector_id, checksum = re.match(r"([a-z\-]+)-(\d+)\[([a-z]{5})\]", line).groups()
        return Room(name, int(sector_id), checksum)

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_room(line.strip()) for line in f.readlines() if line]


def main():
    rooms = parse_input()
    real_rooms = [r for r in rooms if r.is_real]
    res_a = sum(r.sector_id for r in real_rooms)
    logger.info(f"Res A {res_a}")
    north_pole_rooms = [r for r in real_rooms if "northpole" in r.decrypted_name]
    logger.info(f"B {north_pole_rooms[0].sector_id}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
