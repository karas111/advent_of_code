import logging


def init_logging(lvl=logging.INFO):
    logging.basicConfig(
        level=lvl,
        format='[%(asctime)s %(levelname)s %(name)s:%(lineno)d]: %(message)s',
        datefmt='%m-%d-%Y %H:%M')
