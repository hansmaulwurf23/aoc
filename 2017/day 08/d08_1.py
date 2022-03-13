import datetime
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
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        r, func, d, cr, op, param = re.match(r'(\w+) (\w+) (-?\d+) if (\w+) ([<>=!]+) (-?\d+)', line).groups()
        d, param = int(d), int(param)
        if conditions[op](regs[cr], param):
            regs[r] = funcs[func](regs[r], d)

print(regs[max(regs, key=lambda x: regs[x])])
print(datetime.datetime.now() - begin_time)
