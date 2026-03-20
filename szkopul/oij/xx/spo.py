import heapq
from collections import defaultdict


class HeapWithDeleteion:
    def __init__(self):
        self._heap = []
        self._deleted = defaultdict(int)

    def get_min(self):
        self._clean_top()
        return self._heap[0]

    def add(self, el):
        heapq.heappush(self._heap, el)

    def remove(self, el):
        self._deleted[el] += 1

    def _clean_top(self):
        while self._heap and self._deleted[self._heap[0]]:
            min_e = heapq.heappop(self._heap)
            self._deleted[min_e] -= 1


def main():
    n = int(input())
    talk = list(map(int, input().split()))
    late = list(map(int, input().split()))

    time = 0
    waits = HeapWithDeleteion()
    waits_l = []
    for i in range(n):
        wait_t = time - late[i]
        waits.add(wait_t)
        waits_l.append(wait_t)
        time += talk[i]

    res = []
    for i in range(n):
        res.append(time - waits.get_min())
        waits.remove(waits_l[i])
        waits.add(time - late[i])
        time += talk[i]
    print(" ".join(map(str, res)))


if __name__ == "__main__":
    main()
