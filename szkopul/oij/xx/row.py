def main():
    n, m = map(int, input().split())
    line = "*" * m
    for y in range(n):
        print(" " * y + line)


if __name__ == "__main__":
    main()
