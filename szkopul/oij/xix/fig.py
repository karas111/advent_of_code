from math import isqrt


def main():
    sqr_remaining = int(input())
    h = isqrt(sqr_remaining)
    w = sqr_remaining // h
    sqr_remaining -= h * w

    res = "P" * w + "D" * h
    if sqr_remaining:
        res += "D"
        res += "L" * sqr_remaining
        res += "G"
    res += "L" * (w - sqr_remaining)
    res += "G" * h
    print(res)


if __name__ == "__main__":
    main()
