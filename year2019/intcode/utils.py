
def read_program(path):
    with open(path) as f:
        program = [int(n) for n in f.readline().split(",")]
    return program
