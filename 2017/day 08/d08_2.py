import datetime
import math
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

conditions = {
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b
}

funcs = {
    'inc': lambda a, d: a + d,
    'dec': lambda a, d: a - d
}

regs = defaultdict(lambda: 0)
max_reg_val = -math.inf
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        r, func, d, cr, op, param = re.match(r'(\w+) (\w+) (-?\d+) if (\w+) ([<>=!]+) (-?\d+)', line).groups()
        d, param = int(d), int(param)
        if conditions[op](regs[cr], param):
            regs[r] = funcs[func](regs[r], d)
            if regs[r] > max_reg_val:
                max_reg_val = regs[r]

print(max_reg_val)
print(datetime.datetime.now() - begin_time)
