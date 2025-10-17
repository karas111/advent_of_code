import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

SCORE = {c: ord + 1 for ord, c in enumerate("RPS")}


def is_draw(x: tuple[str, str]) -> bool:
    return x[0] == x[1]


def is_win(x: tuple[str, str]) -> bool:
    enemy, me = x
    return (
        (me == "R" and enemy == "S")
        or (me == "S" and enemy == "P")
        or (me == "P" and enemy == "R")
    )


def read_games(replace_second: bool) -> list[tuple[str, str]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        l = f.read().strip()
        l = l.replace("A", "R")
        l = l.replace("B", "P")
        l = l.replace("C", "S")
        if replace_second:
            l = l.replace("X", "R")
            l = l.replace("Y", "P")
            l = l.replace("Z", "S")
        return [tuple(ll.split(" ")) for ll in l.split("\n")]


def count_score(game: tuple[str, str]) -> int:
    return is_draw(game) * 3 + is_win(game) * 6 + SCORE[game[1]]


def adjust_game(game: tuple[str, str]) -> tuple[str, str]:
    enemy, outcome = game
    fn_check = {
        "Z": is_win,
        "Y": is_draw,
        "X": lambda game_: not (is_win(game_) or is_draw(game_)),
    }
    for me in "RPS":
        res = (enemy, me)
        if fn_check[outcome](res):
            return res


def main():
    games = read_games(replace_second=True)
    scores = [count_score(game) for game in games]
    logger.info("Result a %d", sum(scores))

    games = read_games(replace_second=False)
    games = [adjust_game(game) for game in games]
    scores = [count_score(game) for game in games]
    logger.info("Result b %d", sum(scores))


if __name__ == "__main__":
    init_logging()
    main()
    main()
