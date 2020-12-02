import os

def read_numbers():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        masses = [int(line) for line in f]
    return masses

def find_sum(numbers, to_sum):
    for i in range(len(numbers)-1):
        for j in range(i+1, len(numbers)):
            if numbers[i] + numbers[j] == to_sum:
                return i, j
    raise ValueError("Not found")


def find_sum2(numbers, to_sum):
    for i in range(len(numbers)-1):
        for j in range(i+1, len(numbers)):
            for k in range(j+1, len(numbers)):
                if numbers[i] + numbers[j] + numbers[k] == to_sum:
                    return i, j, k
    raise ValueError("Not found")
    

def main():
    numbers = read_numbers()
    x, y = find_sum(numbers, to_sum=2020)
    print(f"A {numbers[x]}*{numbers[y]}={numbers[x]*numbers[y]}")
    x, y, z = find_sum2(numbers, to_sum=2020)
    print(f"A {numbers[x]}*{numbers[y]}*{numbers[z]}={numbers[x]*numbers[y]*numbers[z]}")


if __name__ == "__main__":
    main()
