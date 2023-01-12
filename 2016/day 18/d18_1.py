import datetime

begin_time = datetime.datetime.now()

grid = []


def add_row(last_row):
    new_row = list(last_row)
    for i in range(len(last_row)):
        a = '.' if i == 0 else last_row[i - 1]
        c = '.' if i == len(last_row) - 1 else last_row[i + 1]
        if (a == '^' and c == '.') or (c == '^' and a == '.'):
            new_row[i] = '^'
        else:
            new_row[i] = '.'

    return ''.join(new_row)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(line)

while len(grid) < 40:
    grid.append(add_row(grid[-1]))

# print('\n'.join(grid))
print(sum([sum([1 if c == '.' else 0 for c in row]) for row in grid]))
print(datetime.datetime.now() - begin_time)
