import logging
import time
from collections import deque
import itertools

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def is_valid_state(state):
    for floor in state:
        gen = {g for g in floor if g[1] == "G"}
        if len(gen) == 0:
            continue
        chips = {chip for chip in floor if chip[1] == "M"}
        for chip in chips:
            if f"{chip[0]}G" not in gen:
                return False
    return True


def chose_items(items):
    for item in items:
        yield [item]
    for new_items in itertools.combinations(items, 2):
        yield new_items


def repr_state(state, floor):
    items = {}
    for floor_nb, floor_state in enumerate(state):
        for item in floor_state:
            items[item] = floor_nb
    codes = {x[0] for x in items}
    state_repr = [(items[f"{code}M"], items[f"{code}G"]) for code in codes]
    state_repr = tuple(sorted(state_repr)) + (floor,)
    return state_repr


def state_gen(state, floor):
    for items_to_move in chose_items(state[floor]):
        for new_floor in (floor-1, floor+1):
            if new_floor < 0 or new_floor >= 4:
                continue
            if sum(len(state[i]) for i in range(new_floor + 1)) == 0:
                continue
            new_state = list(state)
            new_state[floor] = new_state[floor] - frozenset(items_to_move)
            new_state[new_floor] = new_state[new_floor] | frozenset(items_to_move)
            new_state = tuple(new_state)
            if is_valid_state(new_state):
                yield (new_state, new_floor)


def bfs(init_state, floor=0):
    end_state = (
        frozenset(),
        frozenset(),
        frozenset(),
        frozenset([item for floor in init_state for item in floor]),
    )
    seen_states = set()
    queue = deque([(init_state, floor, 0)])
    while queue:
        state, floor, steps = queue.popleft()
        state_repr = repr_state(state, floor)
        if state == end_state:
            return steps
        if state_repr in seen_states:
            continue
        seen_states.add(state_repr)
        for new_state, new_floor in state_gen(state, floor):
            queue.append((new_state, new_floor, steps + 1))
    raise ValueError("Not found")


def main():
    init_state = (
        frozenset(["PG", "PM"]),
        frozenset(["CG", "XG", "RG", "LG"]),
        frozenset(["CM", "XM", "RM", "LM"]),
        frozenset([]),
    )
    # init_state = (
    #     frozenset(["HM", "LM"]),
    #     frozenset(["HG"]),
    #     frozenset(["LG"]),
    #     frozenset([]),
    # )

    res_a = bfs(init_state)
    logger.info(f"Res A {res_a}")
    init_state = list(init_state)
    init_state[0] = init_state[0] | frozenset(["EG", "EM", "DG", "DM"])
    init_state = tuple(init_state)
    res_b = bfs(init_state)
    logger.info(f"Res A {res_b}")

if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
