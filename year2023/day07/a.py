import logging
import os
import re
from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property, total_ordering
from typing import Counter

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

CARDS = "AKQJT98765432"
CARDS_VALUE = {card: idx for idx, card in enumerate(reversed(CARDS))}

CARDS_VALUE_MOD = {card: idx for idx, card in enumerate(reversed("AKQT98765432J"))}


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


@total_ordering
@dataclass(frozen=True)
class Hand:
    cards: str
    j_wild_card: bool = False

    def __eq__(self, other: "Hand") -> bool:
        return self.cards == other.cards

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type == other.hand_type:
            return self.cards_strength < other.cards_strength
        return self.hand_type.value < other.hand_type.value

    @cached_property
    def cards_strength(self) -> list[int]:
        cards_value = self.j_wild_card and CARDS_VALUE_MOD or CARDS_VALUE
        return list(map(lambda k: cards_value[k], self.cards))

    @cached_property
    def hand_type(self) -> HandType:
        if self.j_wild_card:
            return max(
                Hand(self.cards.replace("J", n_c), j_wild_card=False).hand_type
                for n_c in CARDS
            )
        else:
            return self._hand_type_raw()

    def _hand_type_raw(self) -> HandType:
        occurences = list(sorted(Counter(self.cards).values(), reverse=True))
        if occurences[0] == 5:
            return HandType.FIVE_OF_A_KIND
        elif occurences[0] == 4:
            return HandType.FOUR_OF_A_KIND
        elif occurences[0] == 3 and occurences[1] == 2:
            return HandType.FULL_HOUSE
        elif occurences[0] == 3 and occurences[1] == 1:
            return HandType.THREE_OF_A_KIND
        elif occurences[0] == 2 and occurences[1] == 2:
            return HandType.TWO_PAIRS
        elif occurences[0] == 2 and occurences[1] == 1:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD


def read_input() -> tuple[list[Hand], list[int]]:
    hands, bids = [], []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(r"(\w{5}) (\d+)")
        for l in f:
            hand, bid = re.match(pattern, l).groups()
            hands.append(Hand(hand))
            bids.append(int(bid))
        return hands, bids


def main():
    hands, bids = read_input()
    with catchtime(logger):
        res = list(sorted(zip(hands, bids), key=lambda k: k[0]))
        res = [(idx + 1) * bid for idx, (_, bid) in enumerate(res)]
        logger.info("Res A: %s", sum(res))

        hands = [Hand(h.cards, j_wild_card=True) for h in hands]
        res = list(sorted(zip(hands, bids), key=lambda k: k[0]))
        res = [(idx + 1) * bid for idx, (_, bid) in enumerate(res)]
        logger.info("Res B: %s", sum(res))


if __name__ == "__main__":
    init_logging()
    main()
