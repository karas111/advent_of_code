import itertools


def main():
    numbers = map(int, input().split())

    for a, b in itertools.combinations(numbers, 2):
        if (a + b) % 2 == 0:
            print("TAK")
            print(f"{a} {b}")
            return
    print("NIE")


if __name__ == "__main__":
    main()
