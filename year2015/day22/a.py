import logging
from collections import defaultdict
from typing import Iterable, NamedTuple

import catch_time
from custom_collections import frozendict
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class Spell(NamedTuple):
    mana: int
    dmg: int
    heal: int
    armor: int
    recharge: int
    timer: int


SPELLS = {
    "MM": Spell(53, 4, 0, 0, 0, 1),
    "Drain": Spell(73, 2, 2, 0, 0, 1),
    "Shield": Spell(113, 0, 0, 7, 0, 6),
    "Poison": Spell(173, 3, 0, 0, 0, 6),
    "Recharge": Spell(229, 0, 0, 0, 101, 5),
}


class State(NamedTuple):
    spell_counters: frozendict.FrozenDict[str, int]
    hitpoints: int
    mana: int
    boss_hitpoints: int
    boss_dmg: int

    def possible_spells(self) -> Iterable[str]:
        for spell_str, spell in SPELLS.items():
            if self.spell_counters[spell_str] > 0:
                continue
            if self.mana < spell.mana:
                continue
            yield spell_str


def trigger_spells(state: State) -> tuple[State, int]:

    hitpoints = state.hitpoints
    boss_hitpoints = state.boss_hitpoints
    mana = state.mana
    armor = 0
    for spell_str, spell_counter in state.spell_counters.items():
        if spell_counter <= 0:
            continue
        spell = SPELLS[spell_str]
        hitpoints += spell.heal
        armor += spell.armor
        boss_hitpoints -= spell.dmg
        mana += spell.recharge
    spell_counters = frozendict.FrozenDict(
        {
            spell_str: max(0, counter - 1)
            for spell_str, counter in state.spell_counters.items()
        }
    )
    return (
        State(
            spell_counters=spell_counters,
            hitpoints=hitpoints,
            boss_hitpoints=boss_hitpoints,
            mana=mana,
            boss_dmg=state.boss_dmg,
        ),
        armor,
    )


def simulate(hitpoints: int, mana: int, boss_hitpoints: int, boss_dmg: int, hard: bool):
    state = State(
        frozendict.FrozenDict({k: 0 for k in SPELLS}),
        hitpoints,
        mana,
        boss_hitpoints,
        boss_dmg,
    )
    result = float("inf")

    def check_win_lost(state: State, used_mana: int) -> bool:
        nonlocal result
        if state.hitpoints <= 0:
            assert state.boss_hitpoints > 0
            return True
        elif state.boss_hitpoints <= 0:
            assert state.hitpoints > 0
            result = min(result, used_mana)
            return True
        return False

    def do_boss(state: State, armor: int, hard: bool) -> State:
        return state._replace(
            hitpoints=state.hitpoints - max(1, state.boss_dmg - armor) - hard
        )

    def do_spell(state: State, spell_str: str) -> State:
        assert state.spell_counters[spell_str] == 0
        spell = SPELLS[spell_str]
        spell_counters = dict(state.spell_counters)
        spell_counters[spell_str] += spell.timer
        mana = state.mana - spell.mana
        assert mana >= 0
        return state._replace(
            spell_counters=frozendict.FrozenDict(spell_counters), mana=mana
        )

    states = {state: 0}
    while states:
        new_states = defaultdict(lambda: float("inf"))
        for org_state, mana_spent in states.items():
            org_state, _ = trigger_spells(org_state)
            if check_win_lost(org_state, mana_spent):
                continue
            for spell_str in org_state.possible_spells():
                new_mana_spent = mana_spent + SPELLS[spell_str].mana
                if new_mana_spent >= result:
                    continue
                state = do_spell(
                    org_state, spell_str
                )  # just increase timer, and spend mana

                state, armor = trigger_spells(state)
                if check_win_lost(state, new_mana_spent):
                    continue
                state = do_boss(state, armor, hard)
                if check_win_lost(state, new_mana_spent):
                    continue
                new_states[state] = min(new_states[state], new_mana_spent)
        states = new_states

    return result


def main():
    # logger.info(
    #     "Res a: %s", simulate(hitpoints=10, mana=250, boss_hitpoints=14, boss_dmg=8)
    # )
    logger.info(
        "Res a: %s",
        simulate(hitpoints=50, mana=500, boss_hitpoints=71, boss_dmg=10, hard=False),
    )
    logger.info(
        "Res b: %s",
        simulate(hitpoints=50, mana=500, boss_hitpoints=71, boss_dmg=10, hard=True),
    )


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
