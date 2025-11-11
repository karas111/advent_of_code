import logging
import os
import re
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Optional

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


class Entry(ABC):

    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def size(self) -> int: ...


class File(Entry):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    @cached_property
    def size(self):
        return self._size

    def __repr__(self):
        return f"<{self.name}>"


class Directory(Entry):
    def __init__(self, name: str, entries: Optional[dict[str, Entry]] = None):
        super().__init__(name)
        self._entries = {} if entries is None else entries

    @cached_property
    def size(self):
        logger.info("use it only after adding all the entries.")
        return sum(entry.size for entry in self._entries.values())

    def add_entry(self, entry: Entry):
        self._entries[entry.name] = entry

    def __repr__(self):
        return f"[{self.name}]"


def read_directories() -> dict[str, Entry]:
    all_directories = {"": Directory("")}
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        cwd = None
        cd_pattern = re.compile(r"^\$ cd (.+)")
        dir_pattern = re.compile(r"dir (.+)")
        file_pattern = re.compile(r"(\d+) (.+)")
        for line in f:
            line = line.strip()
            if m := cd_pattern.match(line):
                param = m.groups()[0]
                if param == "/":
                    cwd = ""
                elif param == "..":
                    cwd = cwd.rsplit("/", maxsplit=1)[0]
                else:
                    cwd = f"{cwd}/{param}"
            elif line == "$ ls":
                ...
            elif m := dir_pattern.match(line):
                name = m.groups()[0]
                full_name = f"{cwd}/{name}"
                new_dir = Directory(full_name)
                if full_name not in all_directories:
                    all_directories[full_name] = new_dir
                all_directories[cwd].add_entry(new_dir)
            elif m := file_pattern.match(line):
                size, name = m.groups()
                all_directories[cwd].add_entry(File(f"{cwd}/{name}", int(size)))
            else:
                raise ValueError(f"Not recongnized command {line}")
    return all_directories


def main():
    directories = read_directories()
    sizes = [x.size for x in directories.values() if x.size <= 100000]
    logger.info("Result a %s", sum(sizes))

    total_space, required_space = 70000000, 30000000
    total_free = total_space - directories[""].size
    sizes = [
        x.size for x in directories.values() if x.size + total_free >= required_space
    ]
    logger.info("Result b %s", min(sizes))


if __name__ == "__main__":
    init_logging()
    main()
