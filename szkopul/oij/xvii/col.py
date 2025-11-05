# START = 931386509544713451
# MAX_STEPS = 2284
# START = 7579309213675935
# MAX_STEPS = 1959
START = 102676904080084950
MAX_STEPS = 1800


def main():
    steps = int(input())
    current_step = MAX_STEPS
    elem = START
    arr = [elem]
    while steps < current_step:
        current_step -= 1
        if elem == 1:
            break
        if elem % 2 == 0:
            elem = elem // 2
        else:
            elem = 3 * elem + 1
        arr.append(elem)
    print(elem)


if __name__ == "__main__":
    main()
