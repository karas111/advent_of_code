import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Cords = tuple[int, int]


def read_input() -> tuple[set[Cords], set[Cords], Cords]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.readlines()
        size = (len(lines[0].strip()), len(lines))
        east_monsters = set()
        south_monsters = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line.strip()):
                if c == "v":
                    south_monsters.add((x, y))
                elif c == ">":
                    east_monsters.add((x, y))
    return east_monsters, south_monsters, size


def swim(east_monsters: set[Cords], south_monsters: set[Cords], size: Cords):
    max_x, max_y = size
    steps = 0
    herds = [(east_monsters, (1, 0)), (south_monsters, (0, 1))]
    while True:
        total_move = 0
        for herd, move in herds:
            new_monsters = {
                ((pos[0] + move[0]) % max_x, (pos[1] + move[1]) % max_y) for pos in herd
            }
            new_monsters -= east_monsters
            new_monsters -= south_monsters
            total_move += len(new_monsters)
            old_monsters = {
                ((monster[0] - move[0]) % max_x, (monster[1] - move[1]) % max_y)
                for monster in new_monsters
            }
            herd -= old_monsters
            herd |= new_monsters
        steps += 1
        if total_move == 0:
            return steps


def main():
    east_monsters, south_monsters, size = read_input()
    res = swim(east_monsters, south_monsters, size)
    logger.info("Res A: %s", res)


if __name__ == "__main__":
    init_logging()
    main()
