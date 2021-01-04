from enum import Enum
from collections import namedtuple

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


MOVE_VEC = {
    Direction.NORTH: (-1, 0),
    Direction.SOUTH: (1, 0),
    Direction.EAST: (0, 1),
    Direction.WEST: (0, -1)
}

DIRECTION_MAP = {
    '^': Direction.NORTH,
    'v': Direction.SOUTH,
    '>': Direction.EAST,
    '<': Direction.WEST
}


class Turns(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1

TURNS = [Turns.LEFT, Turns.STRAIGHT, Turns.RIGHT]

class Cart:

    def __init__(self, direction, x, y):
        self.direction = direction
        self.next_turn_id = 0
        self.x = x
        self.y = y

    def turn(self):
        turn_modifier = TURNS[self.next_turn_id]
        self.next_turn_id += 1
        new_direction_val = self.direction.value + turn_modifier
        if new_direction_val == -1:
            new_direction_val = 3
        elif new_direction_val == 4:
            new_direction_val = 0
        self.direction = Direction(self.direction.value)

    def move(self):
        dx, dy = MOVE_VEC[self.direction]
        self.x += dx
        self.y += dy


def read_field():
    field = []
    carts = []
    with open('input.txt') as f:
        x = 0
        for line in f:
            row = []
            y = 0
            for c in line:
                if c in ['-', '|', '/', '\\', '+', ' ']:
                    row.append(c)
                elif c in ['<', '>']:
                    row.append('-')
                    carts.append(Cart(DIRECTION_MAP[c], x, y))
                elif c in ['^', 'v']:
                    row.append('|')
                    carts.append(Cart(DIRECTION_MAP[c], x, y))
                y += 1
            field.append(row)
            x += 1
    return field, carts


def print_field(field, carts):
    print('\n'.join([''.join(row) for row in field]))

def main():
    field, carts = read_field()
    print_field(field, carts)

if __name__ == '__main__':
    main()
