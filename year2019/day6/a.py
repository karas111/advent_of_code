import os
from cached_property import cached_property


class Node:
    def __init__(self, label):
        self.label = label
        self.neighbours = []
        self.parent = None

    def add_neighbour(self, n):
        self.neighbours.append(n)

    @cached_property
    def orbits(self):
        return sum(n.orbits for n in self.neighbours) + len(self.neighbours)

    def path(self, res=None):
        if res is None:
            res = []
        if self.parent is not None:
            res = self.parent.path(res)
        res.append(self.label)
        return res


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


def calculate1(graph):
    print(sum(n.orbits for n in graph.values()))


def calculate2(graph):
    path1 = graph['YOU'].path()
    path2 = graph['SAN'].path()
    idx = 0
    while path1[idx] == path2[idx]:
        idx += 1
    print(len(path1) + len(path2) - 2 * (idx + 1))


def main():
    graph = read_input()
    calculate1(graph)
    calculate2(graph)


if __name__ == "__main__":
    main()
