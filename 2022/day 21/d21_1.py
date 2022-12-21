import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

mvals = {}
monkeys = {}
dep_on = defaultdict(list)


def monky_op_str(m):
    if isinstance(m, int):
        return str(m)
    elif m in mvals:
        return str(mvals[m])
    else:
        mo = monkeys[m]
        return f"({monky_op_str(mo['a'])}) {mo['op']} ({monky_op_str(mo['b'])})"


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        mid, job = line.split(': ')
        if re.match(r'\d+', job):
            mvals[mid] = int(job)
        else:
            a, op, b = job.split(' ')
            monkeys[mid] = {'op': op, 'a': a, 'b': b}
            dep_on[a].append(mid)
            dep_on[b].append(mid)

print(int(eval(monky_op_str('root'))))
print(datetime.datetime.now() - begin_time)
