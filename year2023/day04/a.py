import logging
import os
import re

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


Card = tuple[set[int], set[int]]


def read_input() -> list[Card]:
    res = []
    pattern = re.compile(r"Card\s+\d+:([\d\s]+)\|([\d\s]+)")
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        matches = re.findall(pattern, f.read())
        res = [
            (set(map(int, match[0].split())), set(map(int, match[1].split())))
            for match in matches
        ]
    return res


def card_point(card: Card) -> int:
    m_winning = len(card[0] & card[1])
    return m_winning and 2 ** (m_winning - 1)

def copy_cards(cards: list[Card]) -> list[int]:
    card_n = [1] * len(cards)
    for idx, card in enumerate(cards):
        n_winning = len(card[0] & card[1])
        for to_add_offset in range(idx+1, idx+1+n_winning):
            card_n[to_add_offset] += card_n[idx]
    return card_n


def main():
    cards = read_input()
    logger.info("Reds A: %s", sum(map(card_point, cards)))
    logger.info("Reds B: %s", sum(copy_cards(cards)))


if __name__ == "__main__":
    init_logging()
    main()
