import bisect


def main():
    _ = int(input())
    zadania = list(map(int, input().split()))
    zadania.sort(reverse=True)

    sumy_prefiksowe = [zadania[0]]
    for punkty in zadania[1:]:
        sumy_prefiksowe.append(sumy_prefiksowe[-1] + punkty)

    sny = int(input())
    for _ in range(sny):
        wymagane_punkty = int(input())
        i = bisect.bisect_left(sumy_prefiksowe, wymagane_punkty)
        print(i+1)
        # start, koniec = 0, len(sumy_prefiksowe)-1
        # while start <= koniec:
        #     srodek = (start + koniec) // 2
        #     if wymagane_punkty > sumy_prefiksowe[srodek]:
        #         start = srodek + 1
        #     else:
        #         koniec = srodek - 1
        # print(start + 1)

if __name__ == "__main__":
    main()