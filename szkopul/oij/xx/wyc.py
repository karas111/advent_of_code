def main():
    m, n = map(int, input().split())
    grid: list[list[int]] = [list(map(int, input().split())) for _ in range(m)]
    res = {}

    def get_neighbours(x, y):
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= nx < n and 0 <= ny < m and grid[ny][nx] > grid[y][x]:
                yield (nx, ny)

    def dfs(x, y):
        stack = [((x, y), False)]
        while stack:
            (x, y), processed = stack.pop()
            if (x, y) in res:
                continue

            if processed:
                res[(x, y)] = max(
                    1, 1, *[1 + res[(nx, ny)] for nx, ny in get_neighbours(x, y)]
                )
            else:
                stack.append(((x, y), True))
                for nx, ny in get_neighbours(x, y):
                    stack.append(((nx, ny), False))

    for x in range(n):
        for y in range(m):
            dfs(x, y)
    print(max(res.values()))


if __name__ == "__main__":
    main()
