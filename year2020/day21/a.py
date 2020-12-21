import copy
import logging
import os
import time
from collections import namedtuple
from typing import Dict, List, Set

from year2019.utils import init_logging

Entry = namedtuple("Entry", ["ingredients", "allergens"])

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> List[Entry]:
    def parse_entry(line: str) -> Entry:
        ingredients, allergens = line.split(" (contains ")
        return Entry(set(ingredients.split(" ")), set(allergens[:-1].split(", ")))

    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_entry(line.strip()) for line in f.readlines() if line]


def possible_allergens(entries: List[Entry]) -> Dict[str, Set[str]]:
    allergen_to_ingredient = {}
    for entry in entries:
        ingredients = entry.ingredients
        for allergen in entry.allergens:
            if allergen in allergen_to_ingredient:
                allergen_to_ingredient[allergen] = (
                    allergen_to_ingredient[allergen] & ingredients
                )
            else:
                allergen_to_ingredient[allergen] = copy.copy(ingredients)
    queue = {
        allergen
        for allergen, ingredients in allergen_to_ingredient.items()
        if len(ingredients) == 1
    }
    matched_allergens = {}
    while queue:
        allergen = queue.pop()
        ingredient = allergen_to_ingredient[allergen].pop()
        del allergen_to_ingredient[allergen]
        matched_allergens[allergen] = ingredient
        for allergen, ing_set in allergen_to_ingredient.items():
            ing_set.discard(ingredient)
            if len(ing_set) == 1:
                queue.add(allergen)
    return matched_allergens, allergen_to_ingredient


def main():
    entries = read_input()
    matched_allergens, possible_matching = possible_allergens(entries)
    all_ings = {ing for entry in entries for ing in entry.ingredients}
    possible_with_allergens = set(matched_allergens.values()) | {
        ing for poss_ings in possible_matching.values() for ing in poss_ings
    }
    without_allergens = all_ings - possible_with_allergens
    res_a = [ing in without_allergens for entry in entries for ing in entry.ingredients]
    logger.info(f"Res A={sum(res_a)}")
    # check if we need some other matching
    assert len(possible_matching) == 0
    sorted_by_allergens = sorted(matched_allergens.items())
    res_b = ",".join(ing for _, ing in sorted_by_allergens)
    logger.info(f'Res B="{res_b}"')


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
