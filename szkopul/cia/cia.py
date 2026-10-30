from collections import Counter


def main():
    _ = input()
    numbers = list(map(int, input().strip().split()))
    counter = Counter(numbers)
    res = 0
    for n in range(10**6, 0, -1):
        to_move = counter.get(n, 0) -1
        if to_move > 0:
            counter[n-1] += to_move
            res += to_move
    print(res)


if __name__ == "__main__":
    main()
