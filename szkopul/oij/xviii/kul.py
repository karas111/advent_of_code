def main():
    n = int(input())
    queue = input()
    time_to_empty = -1
    for idx, c in enumerate(reversed(queue)):
        if c == ".":
            continue
        min_time = idx + 1
        time_to_empty = max(min_time, time_to_empty + 2)
    print(time_to_empty)


if __name__ == "__main__":
    main()
