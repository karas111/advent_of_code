import logging
import os
import time
from functools import lru_cache

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def parse_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [tuple(int(x) for x in line.strip().split("/")) for line in f.readlines() if line]


@lru_cache(maxsize=None)
def brute_force(ports, start, part_b):
    if part_b:
        res = [(0, 0)]
    else:
        res = [0]
    for port in ports:
        if start in port:
            new_ports = frozenset(x for x in ports if x != port)
            new_start = port[(port.index(start) + 1) % 2]
            sub_res = brute_force(new_ports, new_start, part_b)
            if part_b:
                res.append((1 + sub_res[0], sum(port) + sub_res[1]))
            else:
                res.append(sum(port) + sub_res)
    return max(res)


def main():
    ports = parse_input()
    ports_set = frozenset(ports)
    assert len(ports) == len(ports_set)
    res_a = brute_force(ports_set, 0, False)
    logger.info(f"Res A {res_a}")
    res_b = brute_force(ports_set, 0, True)
    logger.info(f"Res B {res_b[1]}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
