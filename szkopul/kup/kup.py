def solve(prices, costs):
    costs_pref = [0]
    for c in costs:
        costs_pref.append(costs_pref[-1] + c)

    def travel_cost(i, j):
        return costs_pref[j] - costs_pref[i]

    res, where_to_sell = 0, 0
    for i in range(len(prices)):
        t_cost = travel_cost(where_to_sell, i)
        gain = prices[where_to_sell] - prices[i] - t_cost
        if res < gain:
            res = gain
        if prices[where_to_sell] - t_cost < prices[i]:
            where_to_sell = i

    return res


def main():
    n = int(input())
    if n == 1:
        print(0)
        return
    prices = list(map(int, input().split()))
    costs = list(map(int, input().split()))
    to_right = solve(prices, costs)
    prices.reverse()
    costs.reverse()
    to_left = solve(prices, costs)
    res = max(to_right, to_left)
    print(res)


if __name__ == "__main__":
    main()
