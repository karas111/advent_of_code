def main():
    trucks = input()
    min_trucks = int(input())
    l_idx, r_idx = 0, -1
    current_trucks = 0
    t = float("inf")
    while True:
        if current_trucks < min_trucks:
            r_idx += 1
            if r_idx >= len(trucks):
                break
            current_trucks += trucks[r_idx] == "X"
        else:
            current_trucks -= trucks[l_idx] == "X"
            l_idx += 1
        if current_trucks >= min_trucks:
            t = min(t, (r_idx - l_idx) / 2)
    print(t)


if __name__ == "__main__":
    main()
