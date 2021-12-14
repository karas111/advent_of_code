from collections import defaultdict
import logging
import os
from typing import Dict, Tuple

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> Tuple[str, Dict[str, str]]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        polymer, instructions_str = f.read().split("\n\n", maxsplit=1)
        instructions = dict(
            line.split(" -> ") for line in instructions_str.split("\n") if line
        )
    return polymer.strip(), instructions


def count_ingredients(polymer: str, instructions: Dict[str, str], steps: int = 10):
    polymer_pairs = [polymer[i:i + 2] for i in range(len(polymer) - 1)]
    polymer_count = defaultdict(lambda: 0)
    for pair in polymer_pairs:
        polymer_count[pair] += 1
    for _ in range(steps):
        new_polymer_count = defaultdict(lambda: 0)
        for pair, count in polymer_count.items():
            insert_ing = instructions[pair]
            new_polymer_count[pair[0] + insert_ing] += count
            new_polymer_count[insert_ing + pair[1]] += count
        polymer_count = new_polymer_count

    count_ing = defaultdict(lambda: 0)
    for pair, count in polymer_count.items():
        count_ing[pair[0]] += count
        count_ing[pair[1]] += count
    # on edges ingredeints are counted once, all others are counted twice
    count_ing[polymer[0]] += 1
    count_ing[polymer[-1]] += 1
    return (max(count_ing.values()) - min(count_ing.values())) // 2


def main():
    polymer, instructions = read_input()
    logger.info(f"Res a {count_ingredients(polymer, instructions, steps=10)}")
    logger.info(f"Res b {count_ingredients(polymer, instructions, steps=40)}")


if __name__ == "__main__":
    init_logging()
    main()
