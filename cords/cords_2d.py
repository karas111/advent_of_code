from dataclasses import dataclass
import math


class Cords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Cords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Cords(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Cords(self.x * scalar, self.y * scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Cords) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Cords({self.x}, {self.y})"
