import logging
import os
from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class ModularFunc:
    def __init__(self, a, b, m):
        super().__init__()
        self.a = a
        self.b = b
        self.m = m

    def shuffle(self, idx):
        return (self.a * idx + self.b) % self.m

    def rev_shuffle(self, idx):
        return (-self.a * idx - self.b)

    def compose(self, mod_func):
        return ModularFunc((self.a * mod_func.a) % self.m, (self.a * mod_func.b + self.b) % self.m, self.m)

    def power(self, n):
        # logger.info('Calculating %d', n)
        if n == 0:
            return ModularFunc(1, 0, self.m)
        y = self.power(n // 2)
        if n % 2 == 0:
            return y.compose(y)
        else:
            return self.compose(y.compose(y))

    def reverse(self):
        a_inv = modinv(self.a, self.m)
        return ModularFunc(a_inv, (-a_inv*self.b) % self.m, self.m)


class Revert(ModularFunc):
    def __init__(self, deck_len):
        super().__init__(-1, -1, deck_len)

    def reverse(self):
        return ModularFunc()


class Cut(ModularFunc):
    def __init__(self, deck_len, cut):
        super().__init__(1, -cut, deck_len)


class DealIncrement(ModularFunc):
    def __init__(self, deck_len, increment):
        super().__init__(increment, 0, deck_len)


def parse_line(line, deck_len):
    line: str = line.strip()
    if line.startswith('deal into new stack'):
        return Revert(deck_len)
    elif line.startswith('cut '):
        return Cut(deck_len, int(line[len('cut '):]))
    elif line.startswith('deal with increment '):
        return DealIncrement(deck_len, int(line[len('deal with increment '):]))
    else:
        raise ValueError()


def read_input(deck_len, test_n=None):
    if test_n is None:
        file_name = 'input.txt'
    else:
        file_name = 'test%d.txt' % test_n
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        shuffles = [parse_line(line, deck_len) for line in f]
    shuffle = shuffles[-1]
    for o_s in shuffles[:-1][::-1]:
        shuffle = shuffle.compose(o_s)
    return shuffle


def shuffle_deck(shuffle, deck):
    deck = {k: k for k in deck}
    for k, idx in deck.items():
        deck[k] = shuffle.shuffle(idx)
    return deck


def print_deck(deck_dict):
    pos_to_card = {v: k for k, v in deck_dict.items()}
    return ' '.join(str(pos_to_card[i]) for i in range(len(pos_to_card)))


def main():
    # logger.info('Starting...')
    # DECK_LEN = 10
    # shuffle = read_input(DECK_LEN, test_n=2)
    # res = shuffle_deck(shuffle, range(DECK_LEN))
    # logger.info('Deck:%s\n', print_deck(res))
    # circle = detect_circle(shuffles, 1)
    # logger.info(circle)

    DECK_LEN = 10007
    CARD = 2019
    shuffles = read_input(DECK_LEN)
    res = shuffle_deck(shuffles, [CARD])
    logger.info('Result part a: %s', res[CARD])

    DECK_LEN = 119315717514047
    SHUFFLED_TIMES = 101741582076661
    POS = 2020
    shuffle = read_input(DECK_LEN)
    shuffle = shuffle.power(SHUFFLED_TIMES)
    shuffle = shuffle.reverse()
    res = shuffle_deck(shuffle, [POS])
    logger.info('Result part b: %s', res[POS])


if __name__ == "__main__":
    init_logging()
    main()
