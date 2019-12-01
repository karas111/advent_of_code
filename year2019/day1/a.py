import os

from testme import ASD

def get_fuel_a(mass):
    return mass // 3 - 2

def get_fuel_b(mass, acc=0):
    fuel_a = get_fuel_a(mass)
    if fuel_a <= 0:
        return acc
    else:
        return get_fuel_b(fuel_a, fuel_a + acc)

def read_masses():
    with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
        masses = [int(line) for line in f]
    return masses

def main():
    masses = read_masses()
    # fuel = [get_fuel_a(mas) for mas in masses]
    fuel = [get_fuel_b(mas) for mas in masses]
    print(sum(fuel))


if __name__ == "__main__":
    main()
