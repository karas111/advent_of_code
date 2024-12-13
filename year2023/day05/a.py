import logging
import os
import re
from typing import Iterable, Mapping

from year2019.utils import init_logging
from sortedcontainers import SortedList


logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class RangeDict:
    def __init__(self, range_to_start: Iterable[tuple[range, int]]):
        self._d = SortedList(range_to_start, key=lambda k: k[0].start)

    def get_ranges(self, key: range) -> list[range]:
        idx = max(self._d.bisect_right((key, -1)) - 1, 0)
        start, stop = key.start, key.stop
        res = []
        while start < stop:
            if idx >= len(self._d):
                res.append(range(start, stop))
                start = stop
                continue
            current_r, map_start = self._d[idx]
            if start > current_r.stop:
                idx += 1
                continue
            if start < current_r.start:
                current_stop = min(current_r.start, stop)
                res.append(range(start, current_stop))
                start = current_stop
                continue
            if start >= current_r.start:
                offset = map_start - current_r.start
                current_stop = min(current_r.stop, stop)
                res.append(range(start + offset, current_stop + offset))
                start = current_stop
                idx += 1
        return res

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)


class LinkedDicts:
    def __init__(self, mappings: Iterable[RangeDict]):
        self._mappings = list(mappings)

    def get_ranges(self, key: range) -> list[range]:
        res = [key]
        for m in self._mappings:
            new_res = []
            for key in res:
                new_res.extend(m.get_ranges(key))
            res = new_res
        return res


def read_input() -> tuple[list[int], LinkedDicts]:
    pattern = re.compile(r"\d+")
    dict_ranges = []
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        seeds = list(map(int, re.findall(pattern, f.readline())))
        f.readline()
        f.readline()
        current_ranges = []
        while True:
            line = f.readline().strip()
            if not line:
                if current_ranges:
                    dict_ranges.append(RangeDict(current_ranges))
                    current_ranges = []
                    if f.readline() == "":
                        break
            else:
                range_ints = list(map(int, line.split()))
                current_ranges.append(
                    (range(range_ints[1], range_ints[1] + range_ints[2]), range_ints[0])
                )
        return seeds, LinkedDicts(dict_ranges)


def main():
    seeds, m_d = read_input()
    res_a = []
    for seed in seeds:
        res_a.extend(m_d.get_ranges(range(seed, seed + 1)))
    logger.info("Res A: %s", min([r.start for r in res_a]))
    res_b = []
    for seed, seed_len in zip(seeds[0::2], seeds[1::2]):
        res_b.extend(m_d.get_ranges(range(seed, seed + seed_len)))
    logger.info("Res B: %s", min([r.start for r in res_b]))


if __name__ == "__main__":
    init_logging()
    main()
