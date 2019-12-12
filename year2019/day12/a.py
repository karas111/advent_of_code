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


def simulate(moons, velcocities, steps=1000):
    for i in range(steps):
        logging.info('After %d steps.\nMoons:\n%s\nVelocities:\n%s', i, moons, velcocities)
        for idx, moon in enumerate(moons):
            vel_v = numpy.sum(moon < moons, axis=0) - numpy.sum(moon > moons, axis=0)
            velcocities[idx] += vel_v
        for idx, moon in enumerate(moons):
            moons[idx] += velcocities[idx]


def total_energy(moons, velocities):
    pot = numpy.sum(numpy.abs(moons), axis=1)
    kin = numpy.sum(numpy.abs(velocities), axis=1)
    return numpy.sum(kin * pot)


def main():
    moons = read_input()
    velocities = numpy.zeros(moons.shape, dtype=int)
    simulate(moons, velocities)
    logging.info('Moons:\n%s\nVelocities:\n%s', moons, velocities)
    res = total_energy(moons, velocities)
    logger.info('Result part a: %s', res)
    res = None
    logger.info('Result part b: %s', res)


if __name__ == "__main__":
    init_logging()
    main()
