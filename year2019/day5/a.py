import os


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        return [x for x in f]


def main():
    read_input()
    pass


if __name__ == "__main__":
    main()
