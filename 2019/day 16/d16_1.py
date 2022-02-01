import datetime
from aopython import last_digit, vector

begin_time = datetime.datetime.now()
base_pattern = [0, 1, 0, -1]


def gen_pattern(pattern, length, expand):
    iter, index, ex = 0, 0, 1
    while iter < length:
        if ex == expand:
            index = (index + 1) % len(pattern)
            ex = 0
        ex += 1
        iter += 1
        yield pattern[index]


# diffs from one line to the next from half down to first
def calc_todos(pattern, lenny):
    todos = dict()
    prev_line = list(gen_pattern(pattern, lenny, lenny // 2 + 1))
    for i in range(lenny // 2, 0, -1):
        cur_line = list(gen_pattern(pattern, lenny, i))
        todo = vector(prev_line, cur_line)
        prev_line = cur_line
        todos[i] = [(i, f) for i, f in enumerate(todo) if f != 0]

    return todos


def phase(numbers, todos):
    lenny = len(numbers)
    out = [0] * lenny
    x = 0
    for i in range(lenny, 0, -1):
        if i > (lenny // 2):
            x += numbers[i - 1]
        else:
            for todo in todos[i]:
                idx, factor = todo
                x += factor * numbers[idx]
        out[i - 1] = last_digit(x)

    return out


with open('./input.txt') as f:
    numbers = list(map(int, f.readlines()[0].rstrip()))

todos = calc_todos(base_pattern, len(numbers))
for i in range(100):
    numbers = phase(numbers, todos)

print(numbers[0:8])
print(datetime.datetime.now() - begin_time)
