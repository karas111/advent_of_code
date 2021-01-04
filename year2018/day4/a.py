import datetime
import logging
import os
import re
import time
from collections import namedtuple
from enum import Enum
from typing import List

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Action(Enum):
    CHANGE_GUARD = 0
    SLEEP = 1
    AWAKE = 2


ACTION_MAP = {
    "falls asleep": Action.SLEEP,
    "wakes up": Action.AWAKE,
}

Note = namedtuple("Note", ["timestamp", "guard", "action"])


def parse_line(line: str) -> Note:
    date, inst = re.match(r"\[(.*)\] (.*)", line).groups()
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    action = ACTION_MAP.get(inst, Action.CHANGE_GUARD)
    if action == Action.CHANGE_GUARD:
        guard = int(re.match(r".* \#(\d*) .*", inst).groups()[0])
        return Note(date, guard, action)
    return Note(date, None, action)


def parse_notes() -> List[Note]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [parse_line(line.strip()) for line in f.readlines() if f]


def get_sleeping_guards(notes: List[Note]):
    res = {}
    current_guard = None
    sleep_time = None
    for note in notes:
        if note.action == Action.CHANGE_GUARD:
            current_guard = note.guard
            if sleep_time is not None:
                raise ValueError("Sleep time shouldnt be none")
            sleep_time = None
        elif note.action == Action.SLEEP:
            sleep_time = note.timestamp
        else:
            res.setdefault(current_guard, []).append((sleep_time, note.timestamp))
            sleep_time = None
    return res


def find_sleeper(guards):
    sleepers = {
        guard: sum((sleep[1] - sleep[0]).seconds // 60 for sleep in sleeps)
        for guard, sleeps in guards.items()
    }
    guard, _ = max(sleepers.items(), key=lambda a: a[1])
    return guard


def find_minute(sleeps):
    res = [0] * 60
    for sleep in sleeps:
        curr_time = sleep[0]
        while curr_time != sleep[1]:
            res[curr_time.minute] += 1
            curr_time += datetime.timedelta(minutes=1)
    return max(res), res.index(max(res))


def res_b(guards):
    most_sleepy_minutes = {
        guard: find_minute(sleeps) for guard, sleeps in guards.items()
    }
    guard, (times_sleep, minute) = max(
        most_sleepy_minutes.items(), key=lambda x: x[1][0]
    )
    return guard * minute


def main():
    notes = parse_notes()
    notes = sorted(notes, key=lambda note: note.timestamp)
    guards = get_sleeping_guards(notes)
    guard = find_sleeper(guards)
    _, minute = find_minute(guards[guard])
    logger.info(f"Res A {guard*minute}")
    logger.info(f"Res B {res_b(guards)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
