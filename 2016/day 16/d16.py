import datetime

begin_time = datetime.datetime.now()


def dragon(a: list):
    b = [1-d for d in reversed(a.copy())]
    a.append(0)
    a.extend(b)
    return a


def checksum(a, disk_size):
    v = a[:disk_size] if len(a) > disk_size else a
    while True:
        v = [1 if a == b else 0 for a, b in zip(v[::2], v[1::2])]
        if len(v) % 2:
            return v


def generate(a, disk_size):
    while len(a) < disk_size:
        a = dragon(a)
    return checksum(a, disk_size)


print(''.join(map(str, generate(list(map(int, '11110010111001001')), 272))))
print(''.join(map(str, generate(list(map(int, '11110010111001001')), 35651584))))
print(datetime.datetime.now() - begin_time)
