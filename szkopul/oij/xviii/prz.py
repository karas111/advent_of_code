from collections import Counter


def main():
    _ = input()
    cards = Counter(map(int, input().split()))
    i = 1
    while True:
        for required in range(i):
            if cards[required] <= 0:
                print(i)
                return
            else:
                cards[required] -= 1
        i += 1


if __name__ == "__main__":
    main()
