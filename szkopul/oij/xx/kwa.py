def main():
    # wczytywanie
    square = []
    for _ in range(5):
        square.append(list(input()))

    res = []
    for y, row in enumerate(square):
        new_r = ""
        for x, c in enumerate(row):
            other_c = square[x][y]
            if c != "?":
                selected_c = c
            else:
                selected_c = other_c
            if other_c != "?" and other_c != selected_c:
                print("NIE")
                return
            if selected_c == "?":
                selected_c = "A"
            new_r += selected_c
        res.append(new_r)

    for row in res:
        print(row)


if __name__ == "__main__":
    main()
