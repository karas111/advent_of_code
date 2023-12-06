import os
import logging

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

NUMBER_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read_lines():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f]


def find_first_number(line: str, with_map: bool, reverse: bool) -> int:
    if reverse:
        line = line[::-1]
    for i in range(len(line)):
        if line[i].isnumeric():
            return int(line[i])
        if with_map:
            for text_val, val in NUMBER_MAP.items():
                if reverse:
                    text_val = text_val[::-1]
                if line[i:].startswith(text_val):
                    return val
    raise ValueError("not found number")


def get_number(line: str, with_map: bool) -> int:
    return 10 * find_first_number(line, with_map, reverse=False) + find_first_number(
        line, with_map, reverse=True
    )


def main():
    lines = read_lines()
    numbers = [get_number(line,  with_map=False) for line in lines]
    logger.info(f"Result a {sum(numbers)}")

    numbers = [get_number(line, with_map=True) for line in lines]
    logger.info(f"Result b {sum(numbers)}")


if __name__ == "__main__":
    init_logging()
    main()
