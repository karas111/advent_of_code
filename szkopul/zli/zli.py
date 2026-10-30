from collections import Counter


def main():
    n = int(input())
    counter = Counter()
    for _ in range(n):
        line = input().strip()
        counter.update(line)
    for k, v in sorted(counter.items()):
        if k.islower():
            print(f"{k} {v}")
    for k, v in sorted(counter.items()):
        if k.isupper():
            print(f"{k} {v}")

if __name__ == "__main__":
    main()
