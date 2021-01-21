import hashlib
import logging
import time

from year2019.utils import init_logging

logger = logging.getLogger(__name__)


def main():
    door_id = "abbhdwsy"
    # door_id = "abc"
    i = 0
    password = ""
    password_b = [None] * 8
    while len(password) < 8 or None in password_b:
        m_hash = hashlib.md5(f"{door_id}{i}".encode()).hexdigest()
        if m_hash.startswith("00000"):
            if len(password) < 8:
                password += m_hash[5]
            if m_hash[5].isdigit() and int(m_hash[5]) < 8 and password_b[int(m_hash[5])] is None:
                password_b[int(m_hash[5])] = m_hash[6]
            logger.info(f"Password {password}, {password_b}")
        i += 1
    password_b = "".join(password_b)
    logger.info(f"Res A {password}")
    logger.info(f"Res B {password_b}")


if __name__ == "__main__":
    init_logging()
    start_time = time.time()
    main()
    logger.info(f"{(time.time() - start_time)*1000} miliseconds ---")
