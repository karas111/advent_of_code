import collections
import logging
import os
import math

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'A(%d, %d)' % (self.x, self.y)

    def __repr__(self):
        return str(self)

    def atan2(self, other):
        return math.atan2(self.y - other.y, self.x - other.x)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "test2.txt")) as f:
        return [Asteroid(x, y) for y, line in enumerate(f.readlines()) for x, c in enumerate(line) if c == '#']


def calculate_visible(asteroid, others):
    grouped_by_angle = collections.defaultdict(list)
    for o_asteroid in others:
        if o_asteroid == asteroid:
            continue
        angle = asteroid.atan2(o_asteroid)
        grouped_by_angle[angle].append(o_asteroid)
    return grouped_by_angle


def find_best_location(asteroids):
    res = {}
    for asteroid in asteroids:
        res[asteroid] = len(calculate_visible(asteroid, asteroids))
    return max(res.items(), key=lambda x: x[1])


def count_nth_asteroid(asteroid, asteroids, counter=200):
    grouped_by_angle = calculate_visible(asteroid, asteroids)
    for a_l in grouped_by_angle.values():
        a_l.sort(key=lambda a: (abs(a.x - asteroid.x), abs(a.y - asteroid.y)))
    grouped_by_angle = list(grouped_by_angle.items())
    grouped_by_angle.sort(key=lambda x: x[0])
    idx = next(x for x, group in enumerate(grouped_by_angle) if group[0] >= math.atan2(1, 0))
    sorted_asteroids = [a_l for angel, a_l in grouped_by_angle]

    res = None
    while counter > 0:
        list_a = sorted_asteroids[idx]
        idx = (idx+1) % len(sorted_asteroids)
        if not list_a:
            continue
        res = list_a.pop(0)
        counter -= 1
    return res


def main():
    asteroids = read_input()
    res = find_best_location(asteroids)
    logger.info('Result part a: %s', res)
    res = count_nth_asteroid(res[0], asteroids)
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    main()
