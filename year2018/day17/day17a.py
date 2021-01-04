

def read_graph():
    data = []
    max_x = 0
    max_y = 0
    min_y = None
    with open('input.txt') as f:
        for line in f:
            coords = line.strip().split(', ')
            if coords[0].startswith('x='):
                x = int(coords[0][2:])
                xx = (x, x)
                yy = tuple(int(y) for y in coords[1][2:].split('..'))
            else:
                y = int(coords[0][2:])
                yy = (y, y)
                xx = tuple(int(y) for y in coords[1][2:].split('..'))
            data.append((xx, yy))
            if xx[1] > max_x:
                max_x = xx[1]
            if yy[1] > max_y:
                max_y = yy[1]
            if min_y is None or min_y > yy[0]:
                min_y = yy[0]
    field = [['.' for j in range(max_y+1)] for i in range(max_x+3)]
    for (x0, x1), (y0, y1) in data:
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                field[x+1][y] = '#'
    # field[0][500] = '+'
    print('x %d, y %d' % (len(field), len(field[0])))
    # print(field[0][500])
    return field, min_y


def print_field(field):
    for y in range(len(field[0])):
        line = ''.join([field[x][y] for x in range(len(field))])
        print(line)
    # print('\n'.join([''.join(row) for row in field]))


def flood(x, y, field, from_up):
    max_x = len(field)
    max_y = len(field[0])
    if field[x][y] != '.':
        return field[x][y] == '|'

    sink = False
    if y + 1 < max_y:
        sink = flood(x, y + 1, field, from_up=True) or sink
    else:
        sink = True

    if not sink:
        field[x][y] = '?'
        if x - 1 >= 0:
            sink = flood(x - 1, y, field, from_up=False) or sink
        else:
            sink = True
        if x + 1 < max_x:
            sink = flood(x + 1, y, field, from_up=False) or sink
        else:
            sink = True

    if sink:
        field[x][y] = '|'
    elif from_up:
        field[x][y] = '~'
    else:
        field[x][y] = '?'

    if from_up:
        sub_x = x - 1
        while sub_x >= 0 and field[sub_x][y] == '?':
            field[sub_x][y] = field[x][y]
            sub_x -= 1
        sub_x = x + 1
        while sub_x < max_x and field[sub_x][y] == '?':
            field[sub_x][y] = field[x][y]
            sub_x += 1
    # print_field(field)
    # print()
    return sink



def main():
    import sys
    sys.setrecursionlimit(10000)
    field, min_y = read_graph()
    flood(501, 0, field, from_up=True)
    print_field(field)
    print()
    print(min_y)
    print(sum(sum(1 if cell in ['~', '|'] and y >= min_y else 0 for y, cell in enumerate(column)) for column in field))
    print(sum(sum(1 if cell in ['~'] and y >= min_y else 0 for y, cell in enumerate(column)) for column in field))


if __name__ == '__main__':
    main()
