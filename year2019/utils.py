import asyncio
import logging


def init_logging(lvl=logging.INFO):
    logging.basicConfig(
        level=lvl,
        format='[%(asctime)s %(levelname)s %(name)s:%(lineno)d]: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S')


def run_main_coroutine(main):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


def print_2dgraph(graph, str_func):
    xs, ys = zip(*graph.keys())
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    lines = []
    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            s = graph.get((x, y))
            if s is None:
                s = ' '
            else:
                if str_func is None:
                    s = str(s)
                else:
                    s = str_func(s)
            line.append(s)
        lines.append(''.join(line))
    return '\n'.join(lines)
