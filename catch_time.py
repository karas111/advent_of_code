from contextlib import contextmanager
from time import perf_counter
from typing import Callable


@contextmanager
def catchtime(logger) -> Callable[[], float]:
    start = perf_counter()
    yield lambda: perf_counter() - start
    logger.info(f"Time: {perf_counter() - start:.3f} seconds")
