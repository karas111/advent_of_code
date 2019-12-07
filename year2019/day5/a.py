import os

from year2019.intcode.computer import Computer
from year2019.intcode.utils import read_program


def main():
    program = read_program(os.path.join(os.path.dirname(__file__), "input.txt"))
    input = [5]
    computer = Computer(program, input, [])
    computer.execute()
    print(computer.output)
    print(program)


if __name__ == "__main__":
    main()
