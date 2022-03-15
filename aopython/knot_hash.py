from collections import deque

NUMLEN = 256
NUMROUNDS = 64


def convert_input(input):
    return list(map(lambda c: ord(c), input.strip())) + [17, 31, 73, 47, 23]


def sparse_hash(lengths):
    numbers = deque(range(NUMLEN))
    cur_pos, skip_size = 0, 0

    for round in range(NUMROUNDS):
        for l in lengths:
            new_numbers = deque()
            for _ in range(l):
                new_numbers.appendleft(numbers.popleft())
            new_numbers.extend(numbers)
            new_numbers.rotate(-l - skip_size)
            cur_pos = (cur_pos + skip_size + l) % NUMLEN
            skip_size += 1
            numbers = new_numbers

    numbers.rotate(cur_pos)
    return list(numbers)


def dense_hash(numbers):
    result = []
    for offset in range(0, NUMLEN, 16):
        result.append(numbers[offset])
        for n in numbers[offset+1:offset+16]:
            result[-1] ^= n

    return result


def hex_hash(bytes):
    return ''.join(map(lambda b: format(b, 'x').rjust(2, '0'), bytes))


def knot_hash(input):
    return dense_hash(sparse_hash(convert_input(input)))


def knot_hash_hex(input):
    return hex_hash(knot_hash(input))
