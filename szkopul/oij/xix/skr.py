def find_shortcut(word, prev_word, next_word):
    def find_short(word1, word2):
        if word2 is None:
            return word1[0]
        res = []
        for c1, c2 in zip(word1, word2):
            res.append(c1)
            if c1 != c2:
                break
        return "".join(res)

    short_1 = find_short(word, next_word)
    short_2 = find_short(word, prev_word)
    return short_1 if len(short_1) > len(short_2) else short_2


def main():
    n = int(input())
    words = []
    for i in range(n):
        words.append((input(), i))
    words.sort()
    shortcuts = [None] * n
    for idx, (word, org_idx) in enumerate(words):
        prev_word = None if idx - 1 < 0 else words[idx - 1][0]
        next_word = None if idx + 1 >= n else words[idx + 1][0]
        shortcuts[org_idx] = find_shortcut(word, prev_word, next_word)
    for w in shortcuts:
        print(w)


if __name__ == "__main__":
    main()
