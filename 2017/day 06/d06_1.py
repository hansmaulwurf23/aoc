import datetime

begin_time = datetime.datetime.now()

seen = set()

def cycle(banks):
    max_val = max(banks)
    idx = banks.index(max_val)
    banks[idx] = 0
    while max_val:
        idx = (idx + 1) % len(banks)
        banks[idx] += 1
        max_val -= 1
    return banks

with open('./input.txt') as f:
    banks = list(map(int, f.readlines()[0].rstrip().split('\t')))

seen.add(tuple(banks))
cycles = 0
while True:
    cycles += 1
    banks = cycle(banks)
    if (t := tuple(banks)) in seen:
        break
    else:
        seen.add(t)

print(cycles)
print(datetime.datetime.now() - begin_time)
