import logging
import os
from typing import NamedTuple, Optional


from catch_time import catchtime
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Range(NamedTuple):
    start: int  # inclusive
    end: int  # exclusive
    file_id: int

    def checksum(self) -> int:
        if self.file_id == -1:
            return 0
        pos_sum = (self.end - 1 + self.start) * (self.end - self.start) // 2
        return pos_sum * self.file_id

    def is_empty(self) -> bool:
        return self.file_id == -1

    def len(self) -> int:
        return self.end - self.start


def read_input() -> list[Range]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        is_file = True
        file_id = 0
        res = []
        last_pos = 0
        for c in f.readline().strip():
            new_length = int(c)
            start, end = last_pos, last_pos + new_length
            if start != end:
                id_to_use = file_id if is_file else -1
                res.append(Range(start, end, id_to_use))
            file_id += is_file
            is_file = not is_file
            last_pos = end
        return res


def rearrgange(ranges: list[Range]) -> list[Range]:
    new_ranges = []
    left_it = iter(ranges)
    right_it = reversed(ranges)
    empty_range = None
    to_move = None
    while True:
        while to_move is None:
            to_move = next(right_it)
            if to_move.is_empty():
                to_move = None
        while empty_range is None:
            empty_range = next(left_it)
            if empty_range.start >= to_move.start:
                break
            if not empty_range.is_empty():
                new_ranges.append(empty_range)
                empty_range = None
        if empty_range.start >= to_move.start:
            new_ranges.append(to_move)
            break
        len_to_move = min(empty_range.len(), to_move.len())
        new_ranges.append(
            Range(empty_range.start, empty_range.start + len_to_move, to_move.file_id)
        )
        empty_range = empty_range._replace(start=empty_range.start + len_to_move)
        if empty_range.len() == 0:
            empty_range = None
        to_move = to_move._replace(end=to_move.end - len_to_move)
        if to_move.len() == 0:
            to_move = None

    return new_ranges


def rearrgange2(ranges: list[Range]) -> list[Range]:
    new_ranges = list(ranges)

    def find_empty_range(range_: Range) -> Optional[tuple[int, Range]]:
        for idx, empty_range in enumerate(new_ranges):
            if empty_range.is_empty() and empty_range.len() >= range_.len():
                return idx, empty_range
        return None

    def remove_range(range_: Range):
        for idx, other_range in reversed(list(enumerate(new_ranges))):
            if other_range.file_id != range_.file_id:
                continue
            other_range = other_range._replace(file_id=-1)
            new_ranges[idx] = other_range
            if (
                idx + 1 < len(new_ranges)
                and new_ranges[idx + 1].is_empty()
                and new_ranges[idx + 1].start == other_range.end
            ):
                other_range = other_range._replace(end=new_ranges[idx + 1].end)
                new_ranges[idx] = other_range
                del new_ranges[idx + 1]
            if (
                idx - 1 >= 0
                and new_ranges[idx - 1].is_empty()
                and new_ranges[idx - 1].end == other_range.start
            ):
                new_prev = new_ranges[idx - 1]._replace(end=other_range.end)
                new_ranges[idx - 1] = new_prev
                del new_ranges[idx]
            return

    for to_move in reversed(ranges):
        if to_move.is_empty():
            continue
        empty_range_id = find_empty_range(to_move)
        if empty_range_id is None:
            continue
        idx, empty_range = empty_range_id
        if empty_range.start > to_move.start:
            continue
        new_ranges[idx] = Range(
            empty_range.start, empty_range.start + to_move.len(), to_move.file_id
        )
        new_empty = Range(empty_range.start + to_move.len(), empty_range.end, -1)
        if new_empty.start < new_empty.end:
            new_ranges.insert(idx + 1, new_empty)
        remove_range(to_move)

    return new_ranges


def main():
    ranges = read_input()
    with catchtime(logger):
        new_ranges = rearrgange(ranges)
    logger.info("Res A %s", sum(range.checksum() for range in new_ranges))
    with catchtime(logger):
        new_ranges = rearrgange2(ranges)
    logger.info("Res B %s", sum(range.checksum() for range in new_ranges))


if __name__ == "__main__":
    init_logging()
    main()
