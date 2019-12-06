import os


class Node:
    def __init__(self, label):
        self.label = label
        self.neighbours = []
        self.parent = None
        self.orbits = 0

    def add_neighbour(self, n):
        self.neighbours.append(n)


def read_input():
    graph = {}
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        for line in f:
            a, b = [x.strip() for x in line.split(')')]
            a_node, b_node = graph.get(a, Node(a)), graph.get(b, Node(b))
            a_node.add_neighbour(b_node)
            b_node.parent = a_node
            graph[a] = a_node
            graph[b] = b_node
    return graph


def calculate_orbits(node):
    for n in node.neighbours:
        calculate_orbits(n)
    node.orbits += sum(n.orbits for n in node.neighbours) + \
        len(node.neighbours)


def calculate1(graph):
    com = graph['COM']
    calculate_orbits(com)
    print(sum(n.orbits for n in graph.values()))


def generate_path(node, path=None):
    if path is None:
        path = []
    if node is None:
        return path
    else:
        path.append(node.label)
        return generate_path(node.parent, path)


def calculate2(graph):
    path1 = generate_path(graph['YOU'])
    path2 = generate_path(graph['SAN'])
    idx = 1
    while path1[-idx] == path2[-idx]:
        idx += 1
    print(len(path1) + len(path2) - 2 * idx)


def main():
    graph = read_input()
    calculate1(graph)
    calculate2(graph)


if __name__ == "__main__":
    main()
