def main():
    _ = input()
    days = list(map(int, input().split()))
    prefs = [0]
    for day in days:
        prefs.append(prefs[-1] + day)
    n_questions = int(input())
    for _ in range(n_questions):
        l, r = map(int, input().split())
        print(prefs[r] - prefs[l - 1])


if __name__ == "__main__":
    main()
