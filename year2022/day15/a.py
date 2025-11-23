import logging
import os
import re

from cords.cords_2d import Cords
from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"

Sensor = tuple[Cords, Cords]


def read_sensors() -> list[Sensor]:
    res = []
    pattern = (
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        for line in f:
            sensor_x, sensor_y, beacon_x, beacon_y = map(
                int, re.search(pattern, line).groups()
            )
            res.append((Cords(sensor_x, sensor_y), Cords(beacon_x, beacon_y)))
    return res


def count_covered(sensors: list[Sensor], y_line: int) -> int:
    compressed_ranges = covered_ranges_at_line(sensors, y_line)
    beacons_at_line = {beacon for _, beacon in sensors if beacon.y == y_line}
    res = sum(r[1] - r[0] + 1 for r in compressed_ranges) - len(beacons_at_line)
    return res


def covered_ranges_at_line(sensors: list[Sensor], y_line: int) -> int:
    ranges = []
    for sensor, beacon in sensors:
        max_distance = (sensor - beacon).manhattan_distance
        y_distance = abs(sensor.y - y_line)
        if max_distance < y_distance:
            continue
        dx = max_distance - y_distance
        range_ = sensor.x - dx, sensor.x + dx
        ranges.append(range_)
    ranges.sort()

    compressed_ranges = []
    current = ranges[0]
    for next_range in ranges[1:]:
        if current[1] + 1 < next_range[0]:
            compressed_ranges.append(current)
            current = next_range
        else:
            current = (current[0], max(current[1], next_range[1]))
    compressed_ranges.append(current)
    return compressed_ranges


def find_empty_beacon(sensors: list[Sensor], max_c: int) -> Cords:
    for y_line in range(max_c):
        ranges = covered_ranges_at_line(sensors, y_line)
        if len(ranges) >= 2:
            logger.info("Found multi ranges %s at line %d", ranges, y_line)
            return Cords(ranges[0][1] + 1, y_line)
        range_ = ranges[0]
        if range_[0] > 0 or range_[1] < max_c:
            raise ValueError("Most likely not that result :)")


def main():
    sensors = read_sensors()
    res = count_covered(sensors, 2000000)
    cords = find_empty_beacon(sensors, 4000000)
    # res = count_covered(sensors, 10)
    # cords = find_empty_beacon(sensors, 20)

    logger.info("Result a %s", res)
    logger.info("Result a %s", cords.x * 4000000 + cords.y)


if __name__ == "__main__":
    init_logging()
    main()
