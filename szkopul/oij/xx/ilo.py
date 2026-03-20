def main():
    _ = int(input())
    numbers = list(map(int, input().split()))

    def solve(k):
        cnt, res = 0, []
        for x in numbers:
            div = x % k == 0
            res.append(x + div)
            cnt += div
        return cnt, res

    chng2, res2 = solve(2)
    chng3, res3 = solve(3)
    chng, res = (chng2, res2) if chng2 < chng3 else (chng3, res3)
    print(chng)
    print(" ".join(str(x) for x in res))


if __name__ == "__main__":
    main()
