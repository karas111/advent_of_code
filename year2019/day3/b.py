import os

TRANSFORM_DIRECTION = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def transform_line(line_str):
    for data in line_str.split(','):
        yield (TRANSFORM_DIRECTION[data[0]], int(data[1:]))


def read_wires():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [list(transform_line(line)) for line in f]


def get_wire_points(wire_direction, starting_point=(0, 0)):
    steps = 0
    points = {}
    for modifier, length in wire_direction:
        for i in range(length):
            starting_point = (starting_point[0] + modifier[0], starting_point[1] + modifier[1])
            steps += 1
            if starting_point not in points:
                points[starting_point] = steps
    return points


def calculate_distance(points, steps_dicts):
    return [sum(steps[point] for steps in steps_dicts) for point in points]


def main():
    wires = read_wires()
    wires_points = [get_wire_points(wire) for wire in wires]
    common_points = wires_points[0].keys()
    for wire_points in wires_points[1:]:
        common_points = common_points & wire_points.keys()
    print(common_points)
    distances = calculate_distance(common_points, wires_points)
    print(min(distances))


if __name__ == "__main__":
    main()
