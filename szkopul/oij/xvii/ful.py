from collections import Counter


def main():
    cards = Counter(input())
    counts = Counter(cards.values())
    fulls = -1
    for triples_from_triples in range(counts[3] + 1):
        for triples_from_quarts in range(counts[4] + 1):
            pairs = (
                counts[2]
                + (counts[3] - triples_from_triples)
                + (counts[4] - triples_from_quarts) * 2
            )
            triples = triples_from_triples + triples_from_quarts
            current_fulls = min(pairs, triples)
            fulls = max(fulls, current_fulls)
    print(fulls)


if __name__ == "__main__":
    main()
