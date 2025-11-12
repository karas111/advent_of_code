from collections import defaultdict


def main():
    number, k = input().split()
    k = int(k)
    # ile razy wystepuje kazda z cyfr od 0-9
    counter = tuple(number.count(str(x)) for x in range(10))

    # bedziemy budowac slownik stanow
    # kluczami sa 10-elementowe krotki
    # kazda oznacza ile razy dana cyfra zostala uzyta do tej pory
    # wartosciami są listy, pod indeksem i-tym w liscie trzymamy
    # ile razy otrzymalismy reszte z dzielenia rowna "i" uzywajac cyfr z klucza
    # np. dla k = 5
    # (2, 0, 0, 0, 0, 0, 1, 0, 0, 0) -> [2, 1, 0, 0, 0] oznacza, ze
    # uzywajac cyfr 0, 0, 6 mozemy otrzymac:
    # - 2 razy reszte 0
    # - 1 raz reszte 1
    # Zaczynamy od nieuzywania zadnej cyfry, wtedy mamy jedna reszte z dzielenia - 0 (bo 0 % k = 0)
    # (0, 0, 0, 0, 0, 0, 0, 0, 0, 0) -> [1, 0, 0..]
    states = {(0,) * 10: [1, *[0] * k]}

    # bedziemy dokladac po 1 cyfrze, az wykorzystamy wszystkie
    for _ in range(len(number)):
        # do nastepnego kroku beda potrzebne nam tylko nowe stane - "wydluzone" o 1 cyfre
        new_states = defaultdict(lambda: [0] * k)

        # iterujemy po wszystkich stanach i do kazdego probojemy dokleic cyfre od 0 do 9
        for state, mods in states.items():
            for d in range(10):
                # jesli juz uzlismy wszystkie cyfry danego typu, przerywamy
                if state[d] + 1 > counter[d]:
                    continue
                # nowy stan jest taki sam jak poprzedni
                # ale ilosc uzycia cyfry "d" jest o 1 wieksza
                new_state = list(state)
                new_state[d] += 1
                new_state = tuple(new_state)
                current_mods = new_states[new_state]
                # tworzymy nowa liste reszt z dzielenia i ich ilosc wystapien
                for mod, mod_n in enumerate(mods):
                    new_mod = (10 * mod + d) % k
                    current_mods[new_mod] += mod_n
        states = new_states
    # wynikiem jest ilosc liczb przy wykorzystaniu wszystkich cyfr, ktorej daja reszte 0
    print(states[counter][0])


if __name__ == "__main__":
    main()
