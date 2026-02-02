def main():
    word = input()
    stacks = [[] for _ in range(ord("z") - ord("a") + 1)]
    res = list(word)
    for i, c in enumerate(word):
        if c != "d":
            stacks[ord(c) - ord("a")].append(i)
        else:
            res[i] = None
            for stack in stacks[::-1]:
                if stack:
                    other_i = stack.pop()
                    res[other_i] = None
                    break
    res = [c for c in res if c is not None]
    print("".join(res))


if __name__ == "__main__":
    main()
