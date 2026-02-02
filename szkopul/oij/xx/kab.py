def main():
    # wczytywanie
    n = int(input())
    sockets = []
    for _ in range(2 * n):
        cords = map(int, input().split())
        sockets.append(tuple(cords))

    # sortujemy
    sockets.sort()

    # bierzemy 2 sąsiadujące
    for i in range(0, len(sockets), 2):
        print(f"{sockets[i][0]} {sockets[i][1]} {sockets[i+1][0]} {sockets[i+1][1]}")


if __name__ == "__main__":
    main()
