import datetime
from collections import deque

begin_time = datetime.datetime.now()
T_LITERAL = 4


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
        while True:
            pckt = read_bits(5)
            if pckt[0] == '0':
                break
    else:
        lentype = read_bits(1)
        if lentype == '0':
            sub_len = read_int(15)
            lb = get_left_bits()
            while get_left_bits() > lb - sub_len:
                version += read_packet()

        elif lentype == '1':
            sub_count = read_int(11)
            for _ in range(sub_count):
                version += read_packet()

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
