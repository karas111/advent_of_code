def main():
    art_n = int(input())
    z_n = art_n // 26
    res = "z" * z_n
    if art_n % 26 != 0:
        res = res + chr(ord("a") + (art_n % 26) - 1)
    print(res)


if __name__ == "__main__":
    main()
