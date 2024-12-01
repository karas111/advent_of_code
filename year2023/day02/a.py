import os
import logging
from typing import Dict, List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

MAX_SHOWDOWN = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game(line: str) -> List[Dict]:
    res = []
    line = line.split(":")[1].strip()
    for showdown_str in line.split("; "):
        showdown = {}
        for token in showdown_str.split(", "):
            n, name = token.split(" ")
            showdown[name] = int(n)
        res.append(showdown)
    return res


def read_games():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return dict(enumerate(parse_game(line.strip()) for line in f))


def check_game(game: List[Dict]) -> bool:
    for showdown in game:
        for color, n in showdown.items():
            if n > MAX_SHOWDOWN[color]:
                return False
    return True


def get_power(game: List[Dict]) -> int:
    res = 1
    for color in ["red", "green", "blue"]:
        res *= max(showdown.get(color, 0) for showdown in game)
    return res


def main():
    games = read_games()
    valid_games = [i + 1 for i, game in games.items() if check_game(game)]
    logger.info(f"Result a {sum(valid_games)}, {valid_games}")

    powers = [get_power(game) for game in games.values()]
    logger.info(f"Result b {sum(powers)}, {powers}")


if __name__ == "__main__":
    init_logging()
    main()
