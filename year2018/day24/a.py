import copy
import logging
import os
import re
import time
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Group:
    def __init__(
        self,
        is_infection,
        units,
        hit_points,
        attack_dmg,
        attack_type,
        initiative,
        weaknesses,
        immunities,
    ) -> None:
        self.is_infection = is_infection
        self.units = units
        self.hit_points = hit_points
        self.attack_dmg = attack_dmg
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    @property
    def effective_power(self):
        return self.units * self.attack_dmg

    @staticmethod
    def parse(line: str, is_infection: bool) -> "Group":
        tmpl = r"^(\d*) units each with (\d*) hit points ((?:\(.*\))|).?with an attack that does (\d*) (\w*) damage at initiative (\d*)$"
        units, hit_poinst, wi_l, attack_dmg, attack_type, initiative = re.match(
            tmpl, line
        ).groups()
        weaknesses, immunities = [], []
        for subline in wi_l.strip("()").split("; "):
            if subline.startswith("weak to "):
                weaknesses += subline[len("weak to ") :].split(", ")
            elif subline.startswith("immune to "):
                immunities += subline[len("immune to ") :].split(", ")
        return Group(
            is_infection,
            int(units),
            int(hit_poinst),
            int(attack_dmg),
            attack_type,
            int(initiative),
            weaknesses,
            immunities,
        )

    def dmg_for_selection(self, defender: "Group") -> int:
        if self.is_infection == defender.is_infection:
            return 0
        if self.attack_type in defender.immunities:
            return 0
        if self.attack_type in defender.weaknesses:
            return 2 * self.effective_power
        return self.effective_power

    def take_dmg(self, dmg: int):
        self.units = max(0, self.units - dmg // self.hit_points)
        return dmg // self.hit_points

    def __repr__(self) -> str:
        return f"Group(Inf={self.is_infection}, Units={self.units}, HP={self.hit_points}, Attack={self.attack_dmg} {self.attack_type}, I={self.initiative})"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        immune, infection = [
            section.strip().split("\n") for section in f.read().split("\n\n")
        ]
    return [Group.parse(line, False) for line in immune[1:]], [
        Group.parse(line, True) for line in infection[1:]
    ]


def chose_targets(groups: List[Group]) -> List[Group]:
    def sort_key(group: Group):
        return (-group.effective_power, -group.initiative)

    def defender_key(attacker: Group, defender: Group):
        return (
            attacker.dmg_for_selection(defender),
            defender.effective_power,
            defender.initiative,
        )

    res = {}
    groups = sorted(groups, key=sort_key)
    for attacker in groups:
        defenders = sorted(
            (defender_key(attacker, defender), defender)
            for defender in groups
            if defender not in res.values()
        )
        target_key, target = defenders[-1]
        if target_key[0] == 0:
            target = None
        res[attacker] = target
    return res


def attack(groups):
    def sort_key(attacker_defender):
        attacker = attacker_defender[0]
        return -attacker.initiative

    attackers_defenders = sorted(groups.items(), key=sort_key)
    total_units_killed = 0
    for attacker, defender in attackers_defenders:
        if defender is not None and attacker.units:
            total_units_killed += defender.take_dmg(
                attacker.dmg_for_selection(defender)
            )
    return total_units_killed


def simulate(groups: List[Group]):
    total_units_killed = -1
    while (
        len({group.is_infection for group in groups}) == 2 and total_units_killed != 0
    ):
        targets = chose_targets(groups)
        total_units_killed = attack(targets)
        groups = [group for group in groups if group.units]
        # logger.info("Round")
    return groups


def part_b(groups: List[Group], min_boost=0, max_boost=10 ** 6):
    min_boost, max_boost = 0, 10 ** 6
    res = None
    while min_boost + 1 != max_boost:
        n_boost = (min_boost + max_boost + 1) // 2
        boosted_groups = copy.deepcopy(groups)
        for group in boosted_groups:
            if not group.is_infection:
                group.attack_dmg += n_boost
        res = simulate(boosted_groups)
        if any(group.is_infection for group in res):
            min_boost = n_boost
        else:
            max_boost = n_boost
        logger.info(f"Window is ({min_boost}, {max_boost})")
    boost = max_boost
    boosted_groups = copy.deepcopy(groups)
    for group in boosted_groups:
        if not group.is_infection:
            group.attack_dmg += boost
    return simulate(boosted_groups)


def main():
    immune, infection = parse_input()
    groups = immune + infection
    winning_army = simulate(copy.deepcopy(groups))
    logger.info(f"Res A {sum(group.units for group in winning_army)}")
    winning_army = part_b(copy.deepcopy(groups), 31, 33)
    logger.info(f"Res B {sum(group.units for group in winning_army)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
