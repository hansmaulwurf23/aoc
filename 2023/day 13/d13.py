import datetime

begin_time = datetime.datetime.now()


def find_reflection_idx(matrix, equality_threshold=0):
    def equality(a, b):
        return sum([1 if x != y else 0 for x, y in zip(a, b)])

    for m in range(1, len(matrix)):
        if sum([equality(a, b) for a, b in zip(reversed(matrix[:m]), matrix[m:])]) == equality_threshold:
            return m


with open('./input.txt') as f:
    grids = [block.splitlines() for block in f.read().split('\n\n')]


def calc_total(grids, max_diffs):
    vtot, htot = 0, 0
    for gno, grid in enumerate(grids):
        hspl = find_reflection_idx(grid, max_diffs)
        if hspl is None:
            vspl = find_reflection_idx(list(zip(*grid)), max_diffs)
            vtot += vspl if vspl else 0
        else:
            htot += hspl if hspl else 0
    return htot * 100 + vtot


for i in range(2):
    tot = calc_total(grids, i)
    print(f'part {i + 1}: {tot}')
    assert tot in [400, 405, 29165, 32192]

print(datetime.datetime.now() - begin_time)
