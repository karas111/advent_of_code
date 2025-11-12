def main():
    art_n = int(input()) - 1  # numerujemy od 0
    z_n = art_n // 26  # ile razy "z" na poczatku
    res_z = "z" * z_n
    res_last = chr(ord("a") + (art_n % 26))  # ostatnia litera, moze tez być "z"
    print(res_z + res_last)


if __name__ == "__main__":
    main()
