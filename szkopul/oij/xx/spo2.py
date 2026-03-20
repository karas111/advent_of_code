from collections import deque


class MinQueue:
    def __init__(self):
        self._queue = deque()
        self._removed = 0
        self._added = 0

    def get_min(self):
        return self._queue[0][0]

    def append(self, el):
        while self._queue and self._queue[-1][0] > el:
            self._queue.pop()
        self._queue.append((el, self._added))
        self._added += 1

    def pop_left(self):
        if self._queue and self._queue[0][1] == self._removed:
            self._queue.popleft()
        self._removed += 1


def main():
    n = int(input())
    talk = list(map(int, input().split()))
    late = list(map(int, input().split()))

    time = 0
    min_queue = MinQueue()
    for i in range(n):
        wait_t = time - late[i]
        min_queue.append(wait_t)
        time += talk[i]

    res = []
    for i in range(n):
        res.append(time - min_queue.get_min())
        min_queue.pop_left()
        min_queue.append(time - late[i])
        time += talk[i]
    print(" ".join(map(str, res)))


if __name__ == "__main__":
    main()
