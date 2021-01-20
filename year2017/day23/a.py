import logging
import os
import time
from functools import lru_cache

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def sieve_of_eratosthenes(n):
    prime = [True for i in range(n + 1)] 
    p = 2
    while (p * p <= n):
        if prime[p]: 
            for i in range(p * 2, n + 1, p): 
                prime[i] = False
        p += 1
    prime[0] = False
    prime[1] = False
    return {i for i in range(n+1) if prime[i]}


def main():
    b = 65*100 + 10 ** 5
    c = b + 17000
    primes = sieve_of_eratosthenes(c + 1)
    complex = [x for x in range(b, c + 1, 17) if x not in primes]
    logger.info(f"Res B {len(complex)}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
