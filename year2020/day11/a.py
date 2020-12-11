import logging
import os
import time

from year2019.utils import init_logging
from functools import lru_cache

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input():
    grid = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            line = line.strip()
            if line:
                grid.append(f".{line}.")
        grid = ["." * len(grid[0])] + grid + ["." * len(grid[0])]
    return grid


def print_grid(grid):
    grid_str = "\n".join(grid)
    logger.info(f"Grid:\n{grid_str}")


def do_one_step(grid, max_occupied, graph):
    def get_symbol(i, j):
        symbol = grid[i][j]
        if symbol == ".":
            return "."
        count = 0
        for ii, jj in graph[(i, j)]:
            if grid[ii][jj] == "#":
                count += 1
        if symbol == "L" and count == 0:
            return "#"
        elif symbol == "#" and count >= max_occupied:
            return "L"
        return symbol

    new_grid = []
    for i in range(len(grid)):
        new_line = []
        for j in range(len(grid[i])):
            new_line.append(get_symbol(i, j))
        new_grid.append("".join(new_line))
    return new_grid


def play_life(grid, max_occupied, graph):
    state = set()
    while True:
        grid_str = "\n".join(grid)
        if grid_str in state:
            return grid
        state.add(grid_str)
        grid = do_one_step(grid, max_occupied, graph)


def create_graph_a(grid):
    res = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in ("L", "#"):
                res[(i, j)] = [
                    (i + di, j + dj)
                    for di in range(-1, 2)
                    for dj in range(-1, 2)
                    if di != 0 or dj != 0
                ]
    return res


def create_graph_b(grid):

    @lru_cache(maxsize=None)
    def get_neighbour(i, j, di, dj):
        if not (0 <= i+di < len(grid) and 0 <= j+dj < len(grid[0])):
            return None
        if grid[i+di][j+dj] in ("L", "#"):
            return (i+di, j+dj)
        return get_neighbour(i+di, j+dj, di, dj)

    res = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in ("L", "#"):
                directions = [(di, dj) for di in range(-1, 2) for dj in range(-1, 2) if di != 0 or dj != 0]
                neighbours = [get_neighbour(i, j, di, dj)for di, dj in directions]
                res[(i, j)] = [n for n in neighbours if n is not None]
    return res


def main():
    grid = read_input()
    graph = create_graph_a(grid)
    last_grid = play_life(grid, max_occupied=4, graph=graph)
    print_grid(last_grid)
    occupied = "".join(last_grid).count("#")
    logger.info(f"Res A={occupied}")
    graph = create_graph_b(grid)
    last_grid = play_life(grid, max_occupied=5, graph=graph)
    print_grid(last_grid)
    occupied = "".join(last_grid).count("#")
    logger.info(f"Res B={occupied}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
