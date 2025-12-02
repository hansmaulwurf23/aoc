import datetime
begin_time = datetime.datetime.now()


def is_valid(val):
    digits = len(str(val))
    if digits % 2:
        return False

    half = 10 ** (digits // 2)
    hi, lo = divmod(val, half)
    if hi != lo:
        return False

    return True


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def is_more_valid(val):
    digits = len(str(val))
    lens = [i for i in range(1, digits // 2 + 1) if digits % i == 0]

    for l in lens:
        old = None
        for part in chunks(str(val), l):
            if old is not None and part != old:
                break
            old = part
        else:
            return True

    return False

part1, part2 = 0, 0
with open('./input.txt') as f:
    for start, end in [list(map(int, e.split('-'))) for e in f.readline().rstrip().split(',')]:
        for i in range(start, end + 1):
            if is_valid(i):
                part1 += i
                part2 += i
            elif is_more_valid(i):
                part2 += i


print(f'part 1: {part1}')
print(f'part 2: {part2}')
assert part1 in (29818212493, 1227775554)
assert part2 in (37432260594, 4174379265)

print(datetime.datetime.now() - begin_time)
