import logging
import os

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

IMG_HEIGHT = 6
IMG_WIDTH = 25
IMG_SIZE = IMG_HEIGHT * IMG_WIDTH


class Layer:
    def __init__(self, raw_data, width=IMG_WIDTH, height=IMG_HEIGHT):
        assert len(raw_data) == width * height
        self.width = width
        self.height = height
        self.raw_data = raw_data

    def add(self, other_layer):
        for i in range(len(self.raw_data)):
            pixel = self.raw_data[i]
            if pixel == 2:
                self.raw_data[i] = other_layer.raw_data[i]

    def __str__(self):
        PIXEL_MAPPING = {0: ' ', 1: '#', 2: 'X'}
        lines = []
        for i in range(self.height):
            line_range = range(i*self.width, (i+1)*self.width)
            lines.append(''.join([PIXEL_MAPPING[self.raw_data[idx]] for idx in line_range]))
        return '\n'.join(lines)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [int(n) for n in f.readline().strip()]


def parse_layers(raw_data):
    return [Layer(raw_data[i*IMG_SIZE:(i+1)*IMG_SIZE]) for i in range(len(raw_data)//IMG_SIZE)]


def part_a(layers):
    min_layer = min(layers, key=lambda l: l.raw_data.count(0))
    return min_layer.raw_data.count(1) * min_layer.raw_data.count(2)


def part_b(layers):
    result = Layer([2]*IMG_SIZE)
    for layer in layers:
        result.add(layer)
    return result


def main():
    raw_data = read_input()
    layers = parse_layers(raw_data)
    logger.info('Result part a: %d', part_a(layers))
    logger.info('Result part b:\n%s', str(part_b(layers)))


if __name__ == "__main__":
    init_logging()
    main()
