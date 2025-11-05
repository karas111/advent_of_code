def main():
    n_q = int(input())
    fence = input()

    pref_sum, diff = [0], 0
    for c in fence:
        diff += 1 if c == "n" else -1
        pref_sum.append(diff)

    for _ in range(n_q):
        l, r = map(int, input().split())
        diff = pref_sum[r] - pref_sum[l - 1]
        if diff > 0:
            print(f"n {diff}")
        elif diff < 0:
            print(f"z {-diff}")
        else:
            print("labor omnia vincit")


if __name__ == "__main__":
    main()
