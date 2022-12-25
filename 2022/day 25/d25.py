import datetime

begin_time = datetime.datetime.now()

VALUES = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
SYMBOLS = {v: k for k, v in VALUES.items()}


def to_dec(snafu: str):
    # return sum([VALUES[d] * pow(5, i) for i, d in enumerate(reversed(snafu))])

    val = 0
    for d in snafu:
        val = val * 5 + VALUES[d]
    # print(f'{snafu} -> {val}')
    return val


def to_snafu(dec):
    digits = []
    exp = 1
    while pow(5, exp) < dec:
        exp += 1

    while exp:
        exp -= 1
        digits.append(dec // pow(5, exp))
        dec = dec % pow(5, exp)

    print(digits, end=' -> ')
    digits.insert(0, 0)
    for i in range(len(digits) - 1, 0, -1):
        if digits[i] > 2:
            digits[i] = digits[i] - 5
            ri = i - 1
            digits[ri] += 1
            while digits[ri] > 2:
                digits[ri] = digits[ri] - 5
                ri -= 1
                digits[ri] += 1
    print(digits)
    if digits[0] == 0:
        digits.pop(0)
    return ''.join(map(lambda d: SYMBOLS[d], digits))


with open('./input.txt') as f:
    sum = sum(map(lambda line: to_dec(line.rstrip()), f.readlines()))

a = '1=-0-2'
b = '12111'
s = to_dec(a) + to_dec(b)
print(s, to_dec(a), to_dec(b))
print(to_snafu(s))

# print(sum)
# print(to_snafu(sum))
print(datetime.datetime.now() - begin_time)
