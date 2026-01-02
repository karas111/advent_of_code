import itertools
import logging
from typing import NamedTuple

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class Item(NamedTuple):
    name: str
    cost: int
    damage: int
    armor: int


WEAPONS = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMOR = [
    Item("No Armor", 0, 0, 0),
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS = [
    Item("NoRing", 0, 0, 0),
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
]


class Character(NamedTuple):
    hitpoints: int
    damage: int
    armor: 2


def is_win(me: Character, boss: Character) -> bool:
    me_dmg = max(1, me.damage - boss.armor)
    turns_to_kill_boss = (boss.hitpoints + me_dmg - 1) // me_dmg
    boss_dmg = max(1, boss.damage - me.armor)
    turns_to_kill_me = (me.hitpoints + boss_dmg - 1) // boss_dmg
    return turns_to_kill_boss <= turns_to_kill_me


def find_cheapest(boss: Character) -> tuple[int, int]:
    min_cost, max_cost = float("inf"), float("-inf")
    for items in itertools.product(WEAPONS, ARMOR, RINGS, RINGS):
        ring1, ring2 = items[-2:]
        if ring1 == ring2:
            continue
        dmg = sum(item.damage for item in items)
        armor = sum(item.armor for item in items)
        cost = sum(item.cost for item in items)
        me = Character(100, dmg, armor)
        if is_win(me, boss):
            min_cost = min(cost, min_cost)
        else:
            max_cost = max(cost, max_cost)
    return min_cost, max_cost


def main():
    boss = Character(103, 9, 2)
    a, b = find_cheapest(boss)
    logger.info("Res a: %s", a)
    logger.info("Res b: %s", b)


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
