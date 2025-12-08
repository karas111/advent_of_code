import logging
import math
import os
from collections import defaultdict, deque

import matplotlib.pyplot as plt
import networkx as nx

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> dict[str, list[str]]:
    g = defaultdict(set)
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            src, neighbours = line.strip().split(": ")
            for dest in neighbours.split(" "):
                g[src].add(dest)
                g[dest].add(src)
        return g


def draw_graph(g: dict[str, list[str]]):
    G = nx.Graph()
    G.add_nodes_from(g.keys())
    for src, ns in g.items():
        for dst in ns:
            G.add_edge(src, dst)

    pos = nx.spring_layout(G, iterations=100)
    nx.draw(
        G,
        pos,
        arrowstyle="->",
        with_labels=True,
    )
    plt.show()


def solve(g: dict[str, set[str]]) -> list[int]:
    res = []
    stack = [(n, 0) for n in g]
    seen = set()
    while stack:
        node, vis = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        if vis == 0:
            res.append([])
        res[-1].append(node)
        for n in g[node]:
            stack.append((n, 1))
    return res


def main():
    g = read_input()
    # draw_graph(g)
    for src, dst in [("ltn", "trh"), ("psj", "fdb"), ("nqh", "rmt")]:
        g[src].remove(dst)
        g[dst].remove(src)
    res = solve(g)
    logger.info("Res a: %s", math.prod([len(x) for x in res]))


if __name__ == "__main__":
    init_logging()
    with catchtime(logger):
        main()
