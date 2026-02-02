def main():
    input()
    numbers = map(int, input().split())
    cur = 1
    for n in numbers:
        cur = (cur * n) % 6
        if cur == 0:
            print("TAK")
            return
    print("NIE")


if __name__ == "__main__":
    main()
