import heapq


def main():
    word = input()
    q = []
    for i, c in enumerate(word):
        if c != "d":
            heapq.heappush(q, (-ord(c), -i))
        elif q:
            heapq.heappop(q)
    res = []
    while q:
        c, i = heapq.heappop(q)
        res.append((-i, chr(-c)))
    res = [c for _, c in sorted(res)]
    print("".join(res))


if __name__ == "__main__":
    main()
