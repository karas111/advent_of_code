import logging
import math
import os
import time
from typing import Dict, List

import numpy as np
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Tile:
    def __init__(self, idx, img, matching_edges=None) -> None:
        self.idx = idx
        self.img = img
        if matching_edges is None:
            matching_edges = [None] * 4
        self.matching_edges = matching_edges

    def edges(self):
        return [
            self.img[0],
            [line[-1] for line in self.img],
            self.img[-1],
            [line[0] for line in self.img],
        ]

    def flip_vertical(self):
        return Tile(
            idx=self.idx,
            img=list(reversed(self.img)),
            matching_edges=[
                self.matching_edges[2],
                self.matching_edges[1],
                self.matching_edges[0],
                self.matching_edges[3],
            ],
        )

    def rotate(self):
        return Tile(
            idx=self.idx,
            img=rotate_img(self.img),
            matching_edges=(self.matching_edges[3:4] + self.matching_edges[:3]),
        )

    def all_tiles(self):
        res = self
        for _ in range(3):
            yield res
            for _ in range(3):
                res = res.rotate()
                yield res
            res = res.flip_vertical()

    def __str__(self) -> str:
        return f"Tile({self.idx})"

    def __repr__(self) -> str:
        return str(self)


def rotate_img(img):
    return list(zip(*img[::-1]))


def parse_tile(tile_str: str) -> Tile:
    tile_str = tile_str.split("\n")
    tile_id = int(tile_str[0][len("Tile ") : -1])
    tile_str = [list(line.strip()) for line in tile_str[1:]]
    return Tile(tile_id, tile_str)


def read_input() -> List[Tile]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        content = f.read().strip()
    return [parse_tile(tile_str) for tile_str in content.split("\n\n")]


def find_matching(tiles: List[Tile]):
    for tile in tiles:
        tile.matching_edges = []
        for edge in tile.edges():
            matching_tile = None
            flipped_edge = list(reversed(edge))
            for other in tiles:
                if other == tile:
                    continue
                if any(
                    other_edge == edge or other_edge == flipped_edge
                    for other_edge in other.edges()
                ):
                    matching_tile = other.idx
                    break
            tile.matching_edges.append(matching_tile)


def get_matching_edges_arrity(matching_edges: List[int]) -> int:
    return sum(matching_one_edge is not None for matching_one_edge in matching_edges)


def match_tile(tile: Tile, edge: int, tiles: Dict[int, Tile]) -> Tile:
    edge_to_match = tile.edges()[edge]
    other = tiles[tile.matching_edges[edge]]
    for other_rot in other.all_tiles():
        if edge_to_match == other_rot.edges()[(edge + 2) % 4]:
            return other_rot


def find_left_top_corner(tiles: Dict[int, Tile]) -> Tile:
    for tile in tiles.values():
        for tile_rot in tile.all_tiles():
            if (
                tile_rot.matching_edges[3] is None
                and tile_rot.matching_edges[0] is None
            ):
                return tile_rot


def create_img(tiles: Dict[int, Tile]) -> List[str]:
    size = int(math.sqrt(len(tiles)))
    tile_grid = [[None for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if i == 0 and j == 0:
                tile_grid[i][j] = find_left_top_corner(tiles)
            elif j == 0:
                # take bottom
                tile_grid[i][j] = match_tile(tile_grid[i - 1][j], edge=2, tiles=tiles)
            else:
                # take left
                tile_grid[i][j] = match_tile(tile_grid[i][j - 1], edge=1, tiles=tiles)
    img_grid = [[None for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            img_grid[i][j] = np.array(tile_grid[i][j].img)[1:-1, 1:-1]
    sub_res = np.concatenate([np.concatenate(img_grid[i], axis=1) for i in range(size)])
    return sub_res.tolist()


def check_and_mark_monster(monster_img, img, x, y):
    for i in range(len(monster_img)):
        for j in range(len(monster_img[0])):
            monster_ch = monster_img[i][j]
            if monster_ch == "#" and img[x + i][y + j] != "#":
                return
    for i in range(len(monster_img)):
        for j in range(len(monster_img[0])):
            if monster_img[i][j] == "#":
                img[x + i][y + j] = "O"


def find_monster(img: List[str]) -> List[str]:
    monster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    monster = Tile(1, monster)
    for monster_tile in monster.all_tiles():
        monster_img = monster_tile.img
        for i in range(len(img) - len(monster_img) + 1):
            for j in range(len(img[0]) - len(monster_img[0]) + 1):
                check_and_mark_monster(monster_img, img, i, j)
        if any(c == "O" for line in img for c in line):
            return


def main():
    tiles = read_input()
    find_matching(tiles)
    matching_edges_arrity = {
        tile.idx: get_matching_edges_arrity(tile.matching_edges) for tile in tiles
    }
    corners = [idx for idx, arrity in matching_edges_arrity.items() if arrity == 2]
    logger.info(f"Res A={math.prod(corners)}")
    img = create_img({tile.idx: tile for tile in tiles})
    find_monster(img)
    water = [c == "#" for line in img for c in line]
    print("\n".join("".join(line) for line in img))
    logger.info(f"Res B={sum(water)}")
    # full_img = create_img(matching_edges)


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
