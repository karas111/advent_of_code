import logging
import math
import os
import re
from abc import abstractmethod
from collections import Counter, deque
from typing import Iterable

import matplotlib.pyplot as plt
import networkx as nx

from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Module:
    def __init__(self, name: str, outs: list[str]):
        self.name = name
        self.outs = outs
        self.state = None

    @abstractmethod
    def receive_pulse(self, pulse: bool, from_: str) -> Iterable[tuple[str, bool]]: ...

    def emit(self, pulse: bool) -> Iterable[tuple[str, bool]]:
        for out in self.outs:
            yield out, pulse

    def __repr__(self):
        return f"{type(self).__name__}({self.name} -> {self.outs})"


class FlipFlop(Module):
    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.state = False

    def receive_pulse(self, pulse: bool, from_: str) -> Iterable[tuple[str, bool]]:
        if pulse:
            return
        self.state = not self.state
        yield from self.emit(self.state)


class Conjuction(Module):

    def __init__(self, name, outs):
        super().__init__(name, outs)
        self.state = {}

    def init_in_connection(self, name):
        self.state[name] = False

    def receive_pulse(self, pulse: bool, from_: str) -> Iterable[tuple[str, bool]]:
        self.state[from_] = pulse
        out_pulse = all(self.state.values())
        yield from self.emit(not out_pulse)


class Broadcaster(Module):
    DEFAULT_NAME = "broadcaster"

    def receive_pulse(self, pulse: bool, from_: str) -> Iterable[tuple[str, bool]]:
        yield from self.emit(pulse)


def run(modules: dict[str, Module], n_iters: int, part_b=False):

    res = Counter()
    comp_iter = {}
    n_iters = part_b and n_iters**10 or n_iters
    for i in range(n_iters):
        queue = deque([(Broadcaster.DEFAULT_NAME, False, "button")])
        while queue:
            module_name, pulse, from_ = queue.popleft()
            if part_b and module_name in ["vt", "xc", "sk", "kk"] and not pulse:
                comp_iter[module_name] = i + 1
                if len(comp_iter) == 4:
                    logger.info(comp_iter)
                    return math.lcm(*comp_iter.values())
            res[pulse] += 1
            if module_name not in modules:
                continue
            for n_mod, n_pulse in modules[module_name].receive_pulse(pulse, from_):
                queue.append((n_mod, n_pulse, module_name))
    return res[True], res[False]


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        pattern = re.compile(r"([%&]?\w+) -> (.+)")
        res = {}
        conj = set()
        while l := f.readline().strip():
            from_, to = re.match(pattern, l).groups()
            to = to.split(", ")
            if from_ == Broadcaster.DEFAULT_NAME:
                res[from_] = Broadcaster(from_, to)
            elif from_[0] == "%":
                res[from_[1:]] = FlipFlop(from_[1:], to)
            else:
                res[from_[1:]] = Conjuction(from_[1:], to)
                conj.add(from_[1:])

        for module in res.values():
            for out_mod in module.outs:
                if out_mod in conj:
                    res[out_mod].init_in_connection(module.name)
        return res


def draw_modules(modules: dict[str, Module]):
    G = nx.DiGraph()
    color_map = []
    for mod in modules.values():
        for out_mod in mod.outs:
            G.add_edge(mod.name, out_mod)
    for node in G:
        mod = modules.get(node)
        if isinstance(mod, Conjuction):
            color_map.append("blue")
        elif isinstance(mod, FlipFlop):
            color_map.append("red")
        else:
            color_map.append("green")

    pos = nx.spring_layout(G, iterations=100)
    nx.draw(
        G,
        pos,
        node_color=color_map,
        arrowstyle="->",
        with_labels=True,
    )
    plt.show()


def main():
    modules = read_input()
    with catchtime(logger):
        high, low = run(modules, 1000)
        logger.info("Res A: %s", high * low)
    modules = read_input()
    with catchtime(logger):
        logger.info("Res B: %s", run(modules, 1000, part_b=True))
    draw_modules(modules)


if __name__ == "__main__":
    init_logging()
    main()
