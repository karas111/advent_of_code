from collections import defaultdict


def main():
    number, k = input().split()
    k = int(k)
    counter = tuple(number.count(str(x)) for x in range(10))

    states = {(0,) * 10: [1, *[0] * k]}

    for _ in range(len(number)):
        new_states = defaultdict(lambda: [0] * k)
        for state, mods in states.items():
            for d in range(10):
                if state[d] + 1 > counter[d]:
                    continue
                new_state = list(state)
                new_state[d] += 1
                new_state = tuple(new_state)
                current_mods = new_states[new_state]
                for mod, mod_n in enumerate(mods):
                    new_mod = (10 * mod + d) % k
                    current_mods[new_mod] += mod_n
        states = new_states
    print(states[counter][0])


if __name__ == "__main__":
    main()
