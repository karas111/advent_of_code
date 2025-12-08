from collections import defaultdict
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class FindUnion(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self._repr = {x: x for x in iterable}
        self._n_sets = len(self._repr)

    def find(self, x: T) -> T:
        parent = self._repr[x]
        if parent == x:
            return x
        self._repr[x] = self.find(parent)
        return self._repr[x]

    def union(self, x: T, y: T) -> None:
        x_rep = self.find(x)
        y_rep = self.find(y)
        if x_rep == y_rep:
            return
        self._n_sets -= 1
        self._repr[x_rep] = y_rep

    @property
    def n_sets(self):
        return self._n_sets

    def get_sets(self) -> list[set[str]]:
        res = defaultdict(set)
        for x in self._repr:
            res[self.find(x)].add(x)
        return list(res.values())
