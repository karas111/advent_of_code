import logging
import os

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

TRACE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def read_input() -> list[dict[str, int]]:
    res = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            properties = line.strip().split(": ", maxsplit=1)[1].split(", ")
            res.append(
                {k: int(v) for k, v in [prop.split(": ") for prop in properties]}
            )
    return res


def filter_matching(aunts: list[dict[str, int]]) -> list[int]:
    res = []
    for idx, aunt in enumerate(aunts):
        if all(TRACE[k] == v for k, v in aunt.items()):
            res.append(idx)
    return res


def filter_matching_b(aunts: list[dict[str, int]]) -> list[int]:
    res = []
    for idx, aunt in enumerate(aunts):
        is_valid = True
        for prop, v in aunt.items():
            if prop in ["cats", "trees"]:
                is_valid = is_valid and TRACE[prop] < v
            elif prop in ["pomeranians", "goldfish"]:
                is_valid = is_valid and TRACE[prop] > v
            else:
                is_valid = is_valid and TRACE[prop] == v
        if is_valid:
            res.append(idx)
    return res


def main():
    aunts = read_input()
    res = filter_matching(aunts)
    logger.info("Res a: %s", [x + 1 for x in res])
    res = filter_matching_b(aunts)
    logger.info("Res a: %s", [x + 1 for x in res])


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
