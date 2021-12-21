from collections import defaultdict
import logging
from typing import Counter, Iterable, NamedTuple, Tuple, List, Dict
from itertools import product
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


FULL_ROUND_SCORE = (1 + 10) * 10 // 2


def part1(positions: List[int]):
    dice = 0
    scores = [0, 0]
    dice_rolls = 0
    while True:
        for i in range(2):
            rolls = (dice * 2 + 4) * 3 // 2
            dice = (dice + 3) % 100
            dice_rolls += 3
            positions[i] = (positions[i] - 1 + (rolls % 10)) % 10 + 1
            scores[i] += positions[i]
            if scores[i] >= 1000:
                return scores[(i + 1) % 2] * dice_rolls


class PlayerState(NamedTuple):
    position: int
    score: int


class State(NamedTuple):
    players: Tuple[PlayerState, PlayerState]
    move: int


def generate_new_state(state: State) -> Iterable[State]:
    for dice_rolls in product([1, 2, 3], repeat=3):
        dice = sum(dice_rolls)
        player = state.players[state.move]
        new_pos = (player.position + dice - 1) % 10 + 1
        new_score = player.score + new_pos
        new_player = PlayerState(new_pos, new_score)
        if state.move == 0:
            new_state = State(
                players=(new_player, state.players[1]), move=(state.move + 1) % 2
            )
        else:
            new_state = State(
                players=(state.players[0], new_player), move=(state.move + 1) % 2
            )
        yield new_state


MAX_SCORE = 21


def topological_sort(starting) -> Tuple[List[State], Dict[State, Counter]]:
    visited = set()
    res = []
    graph = defaultdict(Counter)

    def bfs(state: State):
        if state in visited:
            return
        visited.add(state)
        if any(state.players[i].score >= MAX_SCORE for i in range(2)):
            res.append(state)
            return
        for new_state in generate_new_state(state):
            graph[state][new_state] += 1
            bfs(new_state)
        res.append(state)

    state = State(
        players=(PlayerState(starting[0], 0), PlayerState(starting[1], 0)), move=0
    )
    bfs(state)
    res.reverse()
    logger.info(f"States {len(res)}")
    return res, graph


def part2(starting):
    sorted_states, graph = topological_sort(starting)
    states_count = Counter()
    states_count[sorted_states[0]] += 1
    for state in sorted_states:
        my_count = states_count[state]
        for new_state, count in graph[state].items():
            states_count[new_state] += my_count * count
    winning_states = [
        state
        for state in sorted_states
        if any(player.score >= MAX_SCORE for player in state.players)
    ]
    winning_split = [
        [state for state in winning_states if state.move == (i + 1) % 2]
        for i in range(2)
    ]
    winnig_count = [
        sum(states_count[state] for state in states) for states in winning_split
    ]
    return max(winnig_count)


def main():
    # test_starting = [4, 8]
    logger.info(f"Res a {part1([1, 6])}")
    logger.info(f"Res b {part2([1, 6])}")


if __name__ == "__main__":
    init_logging()
    main()
