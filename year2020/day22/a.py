import copy
import logging
import os
import time
from collections import namedtuple, deque
from typing import Deque, Dict, List, Set, Tuple
import itertools

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> Tuple[Deque[int]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        players = f.read().strip().split("\n\n")
        players = [[int(line.strip()) for line in player.split("\n")[1:]] for player in players]
        return tuple(deque(player) for player in players)


def get_winner_id(decks, round_cards, recurssion_combat):
    if not recurssion_combat or any(len(decks[i]) < round_cards[i] for i in range(2)):
        return round_cards.index(max(round_cards))
    else:
        new_decks = [deque(itertools.islice(decks[i], 0, round_cards[i])) for i in range(2)]
        return play(new_decks, recurssion_combat)


def play(decks: Tuple[Deque[int]], recursion_combat=True):
    seen_states = set()
    while len(decks[0]) > 0 and len(decks[1]) > 0:
        state = tuple(tuple(deck) for deck in decks)
        if state in seen_states:
            return 0
        seen_states.add(state)
        round_cards = [deck.popleft() for deck in decks]
        winning_id = get_winner_id(decks, round_cards, recursion_combat)
        decks[winning_id].extend([round_cards[winning_id], round_cards[(winning_id+1)%2]])
    return len(decks[0]) == 0 and 1 or 0


def main():
    decks = read_input()
    # import cProfile
    # with cProfile.Profile() as pr:
    winner = play(decks)
    # pr.print_stats()
    winning_deck = decks[winner]
    logger.info(f"Winning deck {winning_deck}")
    score = sum((i+1) * x for i, x in enumerate(reversed(winning_deck)))
    logger.info(f"Score {score}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
