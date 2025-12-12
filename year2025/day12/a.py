import logging
import os
from typing import NamedTuple

import catch_time
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Instruction(NamedTuple):
    w: int
    l: int
    presents: tuple


def read_input() -> dict[str, set]:
    shapes, insts = [], []
    parse_inst = False
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        while line := f.readline():
            if "x" in line:
                parse_inst = True

            if not parse_inst:
                shape = []
                for _ in range(3):
                    shape.append(f.readline().strip())
                shapes.append(shape)
                f.readline()
            else:
                # 49x47: 41 41 34 53 39 32
                wl, presents = line.strip().split(": ")
                w, l = map(int, wl.split("x"))
                presents = list(map(int, presents.split(" ")))
                insts.append(Instruction(w, l, presents))
    return shapes, insts


def main():
    shapes, insts = read_input()
    areas = [sum(line.count("#") for line in shape) for shape in shapes]
    fitting = 0
    to_check = []
    for inst in insts:
        area_needed = sum(
            n_pres * areas[idx] for idx, n_pres in enumerate(inst.presents)
        )
        # definitely not fitting
        if inst.w * inst.l < area_needed:
            continue
        # definitely fitting
        if (inst.w // 3) * (inst.l // 3) >= sum(inst.presents):
            fitting += 1
            continue
        to_check.append(inst)

    logger.info("Possible res a %s. Left to check %d.", fitting, len(to_check))


if __name__ == "__main__":
    init_logging()
    with catch_time.catchtime(logger):
        main()
