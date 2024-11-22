import datetime
from collections import deque
from functools import reduce

begin_time = datetime.datetime.now()
T_LITERAL = 4
T_SUM, T_PROD, T_MIN, T_MAX, T_GT, T_LT, T_EQ = 0, 1, 2, 3, 5, 6, 7


def get_left_bits() -> int:
    global data, bit_buffer
    return len(data) * 4 + len(bit_buffer)


def read_byte() -> str:
    global data
    return bin(int(data.popleft(), 16))[2:].zfill(4)


def read_bits(amount: int) -> str:
    global data, bit_buffer

    while len(bit_buffer) < amount:
        bit_buffer += read_byte()

    result = bit_buffer[:amount]
    bit_buffer = bit_buffer[amount:]
    return result


def read_int(bits: int) -> int:
    return int(read_bits(bits), 2)


def read_packet() -> int:
    version = read_int(3)
    type = int(read_bits(3), 2)
    if type == T_LITERAL:
        literal = ''
        while True:
            ltid = read_bits(1)
            literal += read_bits(4)
            if ltid == '0':
                return int(literal, 2)
    else:
        lentype = read_bits(1)
        sub_packets = []
        if lentype == '0':
            sub_len = read_int(15)
            lb = get_left_bits()
            while get_left_bits() > lb - sub_len:
                sub_packets.append(read_packet())

        elif lentype == '1':
            sub_count = read_int(11)
            for _ in range(sub_count):
                sub_packets.append(read_packet())

        if type == T_SUM:
            return sum(sub_packets)
        elif type == T_PROD:
            return reduce(lambda x, y: x * y, sub_packets)
        elif type == T_MIN:
            return min(sub_packets)
        elif type == T_MAX:
            return max(sub_packets)
        elif type == T_GT:
            return 1 if sub_packets[0] > sub_packets[1] else 0
        elif type == T_LT:
            return 1 if sub_packets[0] < sub_packets[1] else 0
        elif type == T_EQ:
            return 1 if sub_packets[0] == sub_packets[1] else 0

    return version


with open('./input.txt') as f:
    data = deque(f.readline().rstrip())
bit_buffer = ''

# examples
# data = deque('D2FE28')
# data = deque('8A004A801A8002F478')
# data = deque('620080001611562C8802118E34')
# data = deque('C0015000016115A2E0802F182340')
# data = deque('A0016C880162017C3686B18A3D4780')
print(read_packet())
print(datetime.datetime.now() - begin_time)
