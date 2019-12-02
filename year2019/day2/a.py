import copy
import os


def red_program():
    with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
        program = [int(n) for n in f.readline().split(',')]
    return program


def modify_program(program):
    program[1] = 12
    program[2] = 2

def execute_program(program, idx=0):
    while True:
        op_code = program[idx]
        if op_code == 99:
            break
        
        a, b, result = program[idx+1:idx+4]
        if op_code == 1:
            program[result] = program[a] + program[b]
        elif op_code == 2:
            program[result] = program[a] * program[b]
        else:
            raise ValueError()
        idx += 4

def find_val(program):
    for i in range(100):
        for j in range(100):
            test_program = copy.copy(program)
            test_program[1] = i
            test_program[2] = j
            execute_program(test_program)
            if test_program[0] == 19690720:
                return i*100 + j



def main():
    program = red_program()
    modify_program(program)
    # program = [1,1,1,4,99,5,6,0,99]
    # execute_program(program)
    value = find_val(program)
    print(value)

if __name__ == "__main__":
    main()
