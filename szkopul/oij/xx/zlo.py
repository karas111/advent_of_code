def main():
    n = int(input())
    min_k, max_k = -1, n - 1
    for i in range(2, n):
        if n % i != 0:
            min_k = i
            break
    print(f"{min_k} {max_k}")


if __name__ == "__main__":
    main()
