import logging
import os

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> list[list[int]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [list(map(int, line.split())) for line in f]


def reduce_story(story: list[int]) -> list[int]:
    return [x1 - x0 for x0, x1 in zip(story, story[1:])]


def solve(story: list[int]) -> int:
    last_numbers = []
    first_numbers = []

    current_story = story
    while not all(x == 0 for x in current_story):
        last_numbers.append(current_story[-1])
        first_numbers.append(current_story[0])
        current_story = reduce_story(current_story)
    # last_numbers.append(0)

    predicted_n = 0
    for n in reversed(last_numbers):
        predicted_n += n

    predicted_h = 0
    for n in reversed(first_numbers):
        predicted_h = n - predicted_h
    return predicted_h, predicted_n


def main():
    stories = read_input()
    with catchtime(logger):
        res = [solve(story) for story in stories]
        logger.info("Res A: %s", sum(x[1] for x in res))
        logger.info("Res B: %s", sum(x[0] for x in res))


if __name__ == "__main__":
    init_logging()
    main()
