import logging
from enum import Enum
from typing import Iterable, Optional

from catch_time import catchtime
from custom_collections.frozendict import FrozenDict
from graph.a_star import Graph, search_shortest
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class PointState(Enum):
    A = 2  # values are x coords destination
    B = 4
    C = 6
    D = 8


COST = {
    PointState.A: 1,
    PointState.B: 10,
    PointState.C: 100,
    PointState.D: 1000,
}

TOP_POINTS = [
    (0, 0),
    (1, 0),
    (3, 0),
    (5, 0),
    (7, 0),
    (9, 0),
    (10, 0),
]
"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
 """


State = FrozenDict[tuple[int, int], PointState]


class Transitions(Graph):
    def __init__(self, max_y: int):
        self._max_y = max_y

    def _get_valid_room_y(self, point_state: PointState, state: State) -> Optional[int]:
        x = point_state.value
        dest_y = self._get_first_empty_y(x, state)

        # there is no room
        if dest_y == 0:
            return

        # not all amphibious are the same in the room
        if any(
            state.get((x, y)) != point_state for y in range(dest_y + 1, self._max_y + 1)
        ):
            return

        return dest_y

    def _get_first_empty_y(self, x: int, state: State) -> int:
        occupied_y = 1
        while (x, occupied_y) not in state and occupied_y <= self._max_y:
            occupied_y += 1
        return occupied_y - 1

    def _is_top_blocked(self, from_: int, to: int, state: State) -> bool:
        if from_ > to:
            from_ -= 1
        else:
            from_ += 1
        return any((x, 0) in state for x in range(min(from_, to), max(from_, to) + 1))

    def _cost(
        self, from_: tuple[int, int], to: tuple[int, int], point_state: PointState
    ):
        return (abs(to[0] - from_[0]) + abs(to[1] - from_[1])) * COST[point_state]

    def _get_new_state(
        self,
        state: State,
        from_: tuple[int, int],
        to: tuple[int, int],
        point_state: PointState,
    ) -> tuple[State, int]:
        new_state = dict(state)
        del new_state[from_]
        new_state[to] = point_state
        return FrozenDict(new_state), self._cost(from_, to, point_state)

    def neighbours(self, n: State) -> Iterable[tuple[State, int]]:
        state = n
        for cords, point_state in state.items():
            x, y = cords
            if point_state is None:
                logger.info("Should never happeneder that %s is None", cords)
                continue
            if y == 0:
                dest_x = point_state.value
                dest_y = self._get_valid_room_y(point_state, state)
                if dest_y is not None and not self._is_top_blocked(x, dest_x, state):
                    yield self._get_new_state(
                        state, cords, (dest_x, dest_y), point_state
                    )
            else:
                first_empty_y = self._get_first_empty_y(x, state)
                if first_empty_y != y - 1:  # if there is something above this one
                    continue
                for dest_x, dest_y in TOP_POINTS:
                    if not self._is_top_blocked(x, dest_x, state):
                        yield self._get_new_state(
                            state, cords, (dest_x, dest_y), point_state
                        )


def main():
    g = Transitions(max_y=2)
    test_start = FrozenDict({
        (2, 1): PointState.B,
        (2, 2): PointState.A,
        (4, 1): PointState.C,
        (4, 2): PointState.D,
        (6, 1): PointState.B,
        (6, 2): PointState.C,
        (8, 1): PointState.D,
        (8, 2): PointState.A,
    })
    start = FrozenDict({
        (2, 1): PointState.B,
        (2, 2): PointState.D,
        (4, 1): PointState.C,
        (4, 2): PointState.D,
        (6, 1): PointState.C,
        (6, 2): PointState.A,
        (8, 1): PointState.B,
        (8, 2): PointState.A,
    })
    goal = FrozenDict({
        (2, 1): PointState.A,
        (2, 2): PointState.A,
        (4, 1): PointState.B,
        (4, 2): PointState.B,
        (6, 1): PointState.C,
        (6, 2): PointState.C,
        (8, 1): PointState.D,
        (8, 2): PointState.D,
    })
    with catchtime(logger):
        score, _ = search_shortest(start, goal, g)
    logger.info("Res A %s", score)

    g = Transitions(max_y=4)
    test_start = FrozenDict(
        {
            (2, 1): PointState.B,
            (2, 2): PointState.D,
            (2, 3): PointState.D,
            (2, 4): PointState.A,
            (4, 1): PointState.C,
            (4, 2): PointState.C,
            (4, 3): PointState.B,
            (4, 4): PointState.D,
            (6, 1): PointState.B,
            (6, 2): PointState.B,
            (6, 3): PointState.A,
            (6, 4): PointState.C,
            (8, 1): PointState.D,
            (8, 2): PointState.A,
            (8, 3): PointState.C,
            (8, 4): PointState.A,
        }
    )
    start = FrozenDict(
        {
            (2, 1): PointState.B,
            (2, 2): PointState.D,
            (2, 3): PointState.D,
            (2, 4): PointState.D,
            (4, 1): PointState.C,
            (4, 2): PointState.C,
            (4, 3): PointState.B,
            (4, 4): PointState.D,
            (6, 1): PointState.C,
            (6, 2): PointState.B,
            (6, 3): PointState.A,
            (6, 4): PointState.A,
            (8, 1): PointState.B,
            (8, 2): PointState.A,
            (8, 3): PointState.C,
            (8, 4): PointState.A,
        }
    )
    goal = FrozenDict(
        {
            (2, 1): PointState.A,
            (2, 2): PointState.A,
            (2, 3): PointState.A,
            (2, 4): PointState.A,
            (4, 1): PointState.B,
            (4, 2): PointState.B,
            (4, 3): PointState.B,
            (4, 4): PointState.B,
            (6, 1): PointState.C,
            (6, 2): PointState.C,
            (6, 3): PointState.C,
            (6, 4): PointState.C,
            (8, 1): PointState.D,
            (8, 2): PointState.D,
            (8, 3): PointState.D,
            (8, 4): PointState.D,
        }
    )
    with catchtime(logger):
        score, _ = search_shortest(start, goal, g)
    logger.info("Res B %s", score)


if __name__ == "__main__":
    init_logging()
    main()
