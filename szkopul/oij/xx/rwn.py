def main():
    a, b, c = map(int, input().split())
    x, y = map(int, input().split())
    if a * x + b * y == c:
        print("TAK")
    else:
        print("NIE")


if __name__ == "__main__":
    main()
