import math
import logging
import os

import numpy

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def read_input():
    res = []
    to_replace = ' <>=xyz'
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for line in f:
            for c in to_replace:
                line = line.replace(c, '')
            res.append([int(cord) for cord in line.split(',')])
    return numpy.array(res)


def simulate(moons, velocities, max_steps=1000):
    cache = [{}, {}, {}]
    period = [None]*3
    step = 0
    while max_steps is None or step < max_steps:
        for i in range(3):
            if period[i] is not None:
                continue
            t = (tuple(moons[:, i]), tuple(velocities[:, i]))
            if t in cache[i]:
                period[i] = step - cache[i][t]
            cache[i][t] = step
        if all(period) and max_steps is None:
            return period
        for idx, moon in enumerate(moons):
            vel_v = numpy.sum(moon < moons, axis=0) - numpy.sum(moon > moons, axis=0)
            velocities[idx] += vel_v
        for idx, moon in enumerate(moons):
            moons[idx] += velocities[idx]
        step += 1


def total_energy(moons, velocities):
    pot = numpy.sum(numpy.abs(moons), axis=1)
    kin = numpy.sum(numpy.abs(velocities), axis=1)
    return numpy.sum(kin * pot)


def lcm(nums):
    res = 1
    for n in nums:
        res = res * n // math.gcd(res, n)
    return res


def main():
    moons = read_input()
    velocities = numpy.zeros(moons.shape, dtype=int)
    moons_a, velocities_a = numpy.copy(moons), numpy.copy(velocities)
    simulate(moons_a, velocities_a, max_steps=1000)
    logger.info('Moons:\n%s\nVelocities:\n%s', moons_a, velocities_a)
    res = total_energy(moons_a, velocities_a)
    logger.info('Result part a: %s', res)

    periods = simulate(numpy.copy(moons), numpy.copy(velocities), max_steps=None)
    logger.info('Result part b: %d. Periods %s', lcm(periods), str(periods))


if __name__ == "__main__":
    init_logging()
    main()
