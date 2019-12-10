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
