from collections import defaultdict


def main():
    input()
    numbers = list(map(int, input().split()))
    l, r = 0, 0
    shortest = float("inf")
    flavours = defaultdict(int)
    flavours[numbers[l]] += 1
    tasty_colour = None
    while True:
        if tasty_colour is not None:
            remove_colour = numbers[l]
            flavours[remove_colour] -= 1
            if tasty_colour == remove_colour:
                tasty_colour = None
            l += 1
        else:
            r += 1
            if r >= len(numbers):
                break
            add_color = numbers[r]
            flavours[add_color] += 1
            if flavours[add_color] == 3:
                tasty_colour = add_color
        if tasty_colour is not None:
            shortest = min(shortest, r - l + 1)
    if shortest == float("inf"):
        print("NIE")
    else:
        print(shortest)


if __name__ == "__main__":
    main()
