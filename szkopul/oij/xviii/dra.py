from collections import defaultdict


def find_ends(graph):
    return {n for n, neighbours in graph.items() if len(neighbours) == 1}


def main():
    n, m = map(int, input().split())
    graph = defaultdict(set)
    for _ in range(m):
        x, y = map(int, input().split())
        graph[x].add(y)
        graph[y].add(x)
    if len(graph) != n:
        print("NIE")
        return

    ends = find_ends(graph)
    if len(ends) != 4:
        print("NIE")
        return
    if any(len(neighbours) != 3 for n, neighbours in graph.items() if n not in ends):
        print("NIE")
        return
    l_end, r_end = ends.pop(), None
    for r_candidate in ends:
        n_l, n_r = graph[l_end].pop(), graph[r_candidate].pop()
        if n_l in graph[n_r] and n_r in graph[n_l]:
            r_end = r_candidate
            ends.remove(r_end)
            graph[n_l].remove(l_end)
            graph[n_r].remove(r_end)
            graph[n_l].remove(n_r)
            graph[n_r].remove(n_l)
            break
        graph[l_end].add(n_l)
        graph[r_candidate].add(n_r)
    if r_end is None:
        print("NIE")
        return

    res = [(l_end, r_end)]
    l, r = n_l, n_r
    while True:
        res.append((l, r))

        if len(graph[l]) != 1 or len(graph[r]) != 1:
            print("NIE")
            break
        n_l, n_r = graph[l].pop(), graph[r].pop()
        if n_l in ends and n_r in ends:
            res.append((n_l, n_r))
            break
        graph[n_l].remove(l)
        graph[n_l].remove(n_r)
        graph[n_r].remove(r)
        graph[n_r].remove(n_l)
        l, r = n_l, n_r

    print("TAK")
    for l, r in res:
        print(f"{l} {r}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("NIE")
