def main():
    n = int(input())
    kolie = []
    for _ in range(n):
        kolie.append(input().strip())
    kolie.sort(key=lambda kolia: (len(kolia), kolia))
    for kolia in kolie:
        print(kolia)

if __name__ == "__main__":
    main()