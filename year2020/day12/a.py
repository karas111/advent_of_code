import logging
import math
import os
import time
from collections import namedtuple
from enum import Enum

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Position = namedtuple("Position", ["x", "y", "direction"])
PositionB = namedtuple("PositionB", ["x", "y", "dx", "dy"])


class Direction(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)


DIR_TO_ID = {direction: idx for idx, direction in enumerate(Direction)}


class Action:
    def __init__(self, action, number) -> None:
        self.action = action
        self.number = number

    def step(self, position: Position) -> Position:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.action}{self.number}"


class ActionGo(Action):
    def step(self, position: Position) -> Position:
        if self.action == "F":
            vec = position.direction.value
        else:
            vec = Direction[self.action].value
        dx, dy = vec
        return Position(
            position.x + dx * self.number,
            position.y + dy * self.number,
            position.direction,
        )


class ActionTurn(Action):
    def step(self, position: Position) -> Position:
        multiplier = {"L": -1, "R": 1}
        d_turn = self.number // 90 * multiplier[self.action]
        direction_id = (DIR_TO_ID[position.direction] + d_turn) % len(Direction)
        return Position(position.x, position.y, list(Direction)[direction_id])


class ActionGoB(Action):
    def step(self, position: PositionB) -> PositionB:
        if self.action == "F":
            dx, dy = position.dx, position.dy
            return PositionB(
                position.x + dx * self.number,
                position.y + dy * self.number,
                position.dx,
                position.dy,
            )
        else:
            dx, dy = Direction[self.action].value
            return PositionB(
                position.x,
                position.y,
                position.dx + dx * self.number,
                position.dy + dy * self.number,
            )


class ActionTurnB(Action):
    def step(self, position: PositionB) -> PositionB:
        multiplier = {"L": 1, "R": -1}
        angle = math.radians(self.number * multiplier[self.action])
        wx = int(math.cos(angle)) * position.dx - int(math.sin(angle)) * position.dy
        wy = int(math.sin(angle)) * position.dx + int(math.cos(angle)) * position.dy
        return PositionB(position.x, position.y, wx, wy)


def parse_action(line, part_b):
    action = line[0]
    number = int(line[1:])
    if part_b:
        if action in "LR":
            return ActionTurnB(action, number)
        else:
            return ActionGoB(action, number)
    else:
        if action in "LR":
            return ActionTurn(action, number)
        else:
            return ActionGo(action, number)


def read_input(part_b):
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_action(line.strip(), part_b) for line in f if line]


def play(position, actions):
    for action in actions:
        position = action.step(position)
    return position


def main():
    # actions = read_input(part_b=False)
    # pos = play(Position(0, 0, Direction.E), actions)
    # logger.info(f"Res A={pos}, {abs(pos.x) + abs(pos.y)}")
    actions = read_input(part_b=True)
    pos = play(PositionB(0, 0, 10, 1), actions)
    logger.info(f"Res B={pos}, {abs(pos.x) + abs(pos.y)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
