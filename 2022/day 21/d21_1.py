import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

mvals = {}
monkeys = {}
dep_on = defaultdict(list)


def apply_monkey_values():
    global mvals, dep_on, monkeys
    new_vals = dict(mvals)
    while new_vals:
        vals = dict(new_vals)
        new_vals = {}
        for mid, val in vals.items():
            if mid in dep_on:
                for depm in dep_on[mid]:
                    if monkeys[depm]['a'] == mid:
                        monkeys[depm]['a'] = val
                    else:
                        monkeys[depm]['b'] = val

                    if isinstance(monkeys[depm]['a'], int) and isinstance(monkeys[depm]['b'], int):
                        mv = int(eval("monkeys[depm]['a'] " + monkeys[depm]['op'] + " monkeys[depm]['b']"))
                        new_vals[depm] = mv
                        monkeys.pop(depm)

                dep_on.pop(mid)

        mvals |= new_vals


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
# apply_monkey_values()
# print(mvals['root'])
print(datetime.datetime.now() - begin_time)
