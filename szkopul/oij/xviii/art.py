def main():
    art_n = int(input()) - 1
    z_n = art_n // 26
    res_z = "z" * z_n
    res_last = chr(ord("a") + (art_n % 26))
    print(res_z + res_last)


if __name__ == "__main__":
    main()
