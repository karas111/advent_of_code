import logging
import os
from collections import defaultdict

import networkx as nx

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Graph = dict[str, set]


def read_input() -> Graph:
    res = defaultdict(set)
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for l in f:
            a, b = l.strip().split("-")
            res[a].add(b)
            res[b].add(a)
    return res


def solve2(g: Graph) -> str:
    G = nx.Graph()
    for x, neighbours in g.items():
        for y in neighbours:
            G.add_edge(x, y)

    max_clique = None

    for clique in nx.find_cliques(G):
        if max_clique is not None and len(max_clique) >= len(clique):
            continue
        if any(x.startswith("t") for x in clique):
            max_clique = clique
    return ",".join(sorted(max_clique))


def solve2_ver2(g: Graph):
    def bron_kerbosch(r: set, p: set, x: set):
        if not p and not x:
            yield r
        for n in list(p):
            yield from bron_kerbosch(r | {n}, p & g[n], x & g[n])
            p.remove(n)
            x.add(n)

    all_cliques = bron_kerbosch(set(), set(g.keys()), set())
    max_clique = sorted(all_cliques, key=len)[-1]
    return ",".join(sorted(max_clique))


def solve(g: Graph) -> int:
    res = set()
    for x0, neighbours0 in g.items():
        if not x0.startswith("t"):
            continue
        for x1, neighbours1 in g.items():
            if x0 == x1:
                continue
            if x1 not in neighbours0:
                continue
            for x2 in neighbours0 & neighbours1:
                res.add(tuple(sorted([x0, x1, x2])))
    return len(res)


def main():
    g = read_input()
    with catchtime(logger):
        n = solve(g)
        logger.info("Res A: %s", n)
        b = solve2(g)
        logger.info("Res B: %s", b)
        b = solve2_ver2(g)
        logger.info("Res B: %s", b)


if __name__ == "__main__":
    init_logging()
    main()
