import heapq


def main():
    _ = input()
    caves = map(int, input().split())
    seen = []
    current, switches = 0, 0
    for cave in caves:
        heapq.heappush(seen, cave)
        current += cave
        if current < 0:
            to_change = heapq.heappop(seen)
            current += 2 * abs(to_change)
            switches += 1
    print(switches)


if __name__ == "__main__":
    main()
