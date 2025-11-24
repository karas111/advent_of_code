from collections import defaultdict


def main():
    verticals = defaultdict(list)
    x, y = 0, 0
    for c in input():
        if c == "L":
            x -= 1
        elif c == "P":
            x += 1
        elif c == "D":
            verticals[y].append(x)
            y += 1
        else:  # c == "G"
            y -= 1
            verticals[y].append(x)

    area = 0
    for xs in verticals.values():
        xs.sort()
        for start, end in zip(xs[::2], xs[1::2]):
            area += end - start
    print(area)


if __name__ == "__main__":
    main()
