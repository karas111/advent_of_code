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
    res = set()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for y, line in enumerate(f.readlines()):
            for x, c in enumerate(line):
                if c == '#':
                    res.add(Asteroid(x, y))
    return res


def calculate_visible(asteroid, others):
    angles = set()
    for o_asteroid in others:
        if o_asteroid == asteroid:
            continue
        angle = asteroid.atan2(o_asteroid)
        angles.add(angle)
    return len(angles)


def find_best_location(asteroids):
    res = {}
    for asteroid in asteroids:
        res[asteroid] = calculate_visible(asteroid, asteroids)
    logging.info('All visibiles %s', res)
    return max(res.items(), key=lambda x: x[1])


def count_200(asteroid, asteroids):
    angles = collections.defaultdict(list)
    for o_asteroid in asteroids:
        if o_asteroid == asteroid:
            continue
        angle = asteroid.atan2(o_asteroid)
        angles[angle].append(o_asteroid)
    for a_l in angles.values():
        a_l.sort(key=lambda a: (abs(a.x - asteroid.x), abs(a.y - asteroid.y)))
    angles = list(angles.items())
    angles.sort(key=lambda x: x[0])
    # logging.info(angles)
    idx = next(x for x, group in enumerate(angles) if group[0] >= math.atan2(1, 0))
    counter = 200
    res = None
    while counter > 0:
        list_a = angles[idx][1]
        if not list_a:
            idx += 1
            idx %= len(angles)
            continue
        idx += 1
        idx %= len(angles)
        res = list_a.pop(0)
        counter -= 1
    return res



def main():
    asteroids = read_input()
    res = find_best_location(asteroids)
    logger.info('Result part a: %s', res)
    res = count_200(res[0], asteroids)
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    main()
