import logging
import os
import time
import numpy as np
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [tuple(int(x) for x in line.strip().split(",")) for line in f.readlines() if line]


def is_in_constelation(coords, constelation):
    coords = np.array(coords)
    distances = [sum(np.abs(np.array(x) - coords)) for x in constelation]
    return any(d <= 3 for d in distances)


def part_a(coords):
    constelations = []
    for coord in coords:
        all_matching = set()
        for idx, constelation in enumerate(constelations):
            if is_in_constelation(coord, constelation):
                all_matching.add(idx)
        n_constelations = [c for idx, c in enumerate(constelations) if idx not in all_matching]
        n_constelations.append(sum([constelations[idx] for idx in all_matching], [coord]))
        constelations = n_constelations
    return constelations


def main():
    cords = parse_input()
    res_a = part_a(cords)
    logger.info(f"Res A {len(res_a)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
