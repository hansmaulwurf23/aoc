import datetime

begin_time = datetime.datetime.now()

seen = dict()

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

cycles = 0
seen[tuple(banks)] = cycles
while True:
    cycles += 1
    banks = cycle(banks)
    if (t := tuple(banks)) in seen:
        break
    else:
        seen[t] = cycles

print(cycles - seen[t])
print(datetime.datetime.now() - begin_time)
