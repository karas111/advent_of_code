from collections import Counter


def main():
    _ = input()
    numbers = list(map(int, input().strip().split()))
    maxes = []
    for odd in range(2):
        counter = Counter(numbers[odd::2])
        counter = [(enc, n) for n, enc in counter.items()]
        counter.append((0, -1))
        max_ = max(counter)
        max_s = max([x for x in counter if x != max_])
        maxes.append((max_, max_s))

    odd_maxes, even_maxes = maxes
    if odd_maxes[0][1] != even_maxes[0][1]:
        print(len(numbers) - odd_maxes[0][0] - even_maxes[0][0])
    else:
        print(len(numbers) - max(odd_maxes[0][0] + even_maxes[1][0], odd_maxes[1][0] + even_maxes[0][0]))


if __name__ == "__main__":
    main()
