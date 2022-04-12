import datetime
import re

begin_time = datetime.datetime.now()

factors = (16807, 48271)
mask = 2**16 - 1
mod = 2**31 - 1
# rounds = 5
rounds = 40000000

with open('./input.txt') as f:
    gen_vals = []
    while line := f.readline().rstrip():
        gen_vals.append(int(re.findall(r'-?\d+', line)[0]))

# gen_vals = [65, 8921]
matches = 0
for r in range(rounds):
    for i, v in enumerate(gen_vals):
        gen_vals[i] = gen_vals[i] * factors[i] % 2147483647
        # for reasons unknown the shortcut with modulo mersenne numbers is not faster
        # gen_vals[i] = gen_vals[i] * factors[i]
        # gen_vals[i] = (gen_vals[i] >> 31) + (gen_vals[i] & mod)
        # while gen_vals[i] >= mod:
        #     gen_vals[i] = (gen_vals[i] & mod) + (gen_vals[i] >> 31);

    if gen_vals[0] & mask == gen_vals[1] & mask:
        matches += 1

    # print(gen_vals)

print(matches)
print(631)
print(datetime.datetime.now() - begin_time)
