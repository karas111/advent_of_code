MATCHING = {
    ")": "(",
    "}": "{",
    "]": "[",
    ">": "<",
}


def main():
    n = int(input())
    for _ in range(n):
        stack = []
        line = input().strip()
        all_matching = True
        for c in line:
            if c in "({[<":
                stack.append(c)
            elif stack and MATCHING[c] == stack[-1]:
                stack.pop()
            else:
                all_matching = False
                break
        if stack or not all_matching:
            print("N")
        else:
            print("T")


if __name__ == "__main__":
    main()
