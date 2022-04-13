import datetime
import re

begin_time = datetime.datetime.now()

factors = (16807, 48271)
mods = (4, 8)
mask = 2**16 - 1
# rounds = 5
# gen_vals = [65, 8921]
rounds = 5000000

with open('./input.txt') as f:
    gen_vals = []
    while line := f.readline().rstrip():
        gen_vals.append(int(re.findall(r'-?\d+', line)[0]))

matches = 0
for r in range(rounds):
    for i, v in enumerate(gen_vals):
        while True:
            gen_vals[i] = gen_vals[i] * factors[i] % 2147483647
            if gen_vals[i] % mods[i] == 0:
                break

    if gen_vals[0] & mask == gen_vals[1] & mask:
        matches += 1

print(matches)
print(631)
print(datetime.datetime.now() - begin_time)
