import logging
import os
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"
SIZE = 5


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        lines = f.read().split("\n\n")
        numbers = [int(x) for x in lines[0].split(",")]
        boards = []
        for board_str in lines[1:]:
            board_numbers = [
                [int(x) for x in row.strip().split(" ") if x]
                for row in board_str.split("\n")
            ]
            boards.append(Board(board_numbers))
    return numbers, boards


class Board:
    def __init__(self, numbers):
        self.numbers = numbers
        self.checked = [[False] * SIZE for _ in range(SIZE)]

    def mark_number(self, number):
        for y, row in enumerate(self.numbers):
            for x, board_number in enumerate(row):
                if board_number == number:
                    self.checked[y][x] = True
                winning_pos = self.check_winnig_pos(y, x)
                if winning_pos:
                    res = self.calculate_res()
                    return res * number
        return -1

    def check_winnig_pos(self, y, x):
        return all(self.checked[y][x] for x in range(SIZE)) or all(
            self.checked[y][x] for y in range(SIZE)
        )

    def calculate_res(self):
        return sum(
            board_number
            for y, row in enumerate(self.numbers)
            for x, board_number in enumerate(row)
            if not self.checked[y][x]
        )


def play(numbers: List[int], boards: List[Board]):
    for number in numbers:
        for board in boards:
            winning_pos = board.mark_number(number)
            if winning_pos > 0:
                return winning_pos
    raise ValueError("Not found winning")


def play_lose(numbers: List[int], boards: List[Board]):
    for number in numbers:
        new_boards = []
        for board in list(boards):
            winning_pos = board.mark_number(number)
            if winning_pos > 0 and len(boards) == 1:
                return winning_pos
            elif winning_pos < 0:
                new_boards.append(board)
        boards = new_boards
    raise ValueError("Not found winning")


def main():
    numbers, boards = read_input()
    res = play(numbers, boards)
    logger.info(f"Result a {res}")
    res = play_lose(numbers, boards)
    logger.info(f"Result b {res}")


if __name__ == "__main__":
    init_logging()
    main()
