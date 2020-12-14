import logging
import math
import os
import time
from collections import namedtuple
from enum import Enum

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Schedule = namedtuple("Schedule", ["arrival", "ids"])


def read_input():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        arrival = int(f.readline().strip())
        ids = [int(x) for x in f.readline().strip().split(",") if x != "x"]
    return Schedule(arrival, ids)


def read_input_b():
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        _ = f.readline()
        ids = {-idx: int(x) for idx, x in enumerate(f.readline().strip().split(",")) if x!= "x"}
    return ids


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = egcd(b % a, a)
        return (gcd, y - (b//a) * x, x)


def res_b(bus_ids):
    bus_ids = list(bus_ids.items())
    current = bus_ids[0]
    for next_pair in bus_ids[1:]:
        _, f, g = egcd(current[1], next_pair[1])
        current = (current[0] * g * next_pair[1] + next_pair[0] * f * current[1]) % (current[1] * next_pair[1]), current[1] * next_pair[1]
    return current


def calculate_waiting(schedule: Schedule) -> int:
    waits = [((-schedule.arrival) % bus_id, bus_id) for bus_id in schedule.ids]
    return waits


def main():
    schedule = read_input()
    waitings = calculate_waiting(schedule)
    logger.info(f"Waiting {waitings}")
    min_waiting = min(waitings)
    logger.info(f"Res A, {min_waiting}, {min_waiting[0] * min_waiting[1]}")
    bus_ids = read_input_b()
    # bus_ids = {19: 20, 1: 7}
    logger.info(res_b(bus_ids))

if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
