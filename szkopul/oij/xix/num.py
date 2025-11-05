NUM_MAP = {
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
}


def main():
    number = input()
    k = int(input()) - 1
    res = []
    for n in reversed(number):
        all_letters = NUM_MAP[n]
        letter = all_letters[k % len(all_letters)]
        res.append(letter)
        k = k // len(all_letters)
    print("".join(reversed(res)))


if __name__ == "__main__":
    main()
