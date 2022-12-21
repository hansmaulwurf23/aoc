import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

mvals = {}
monkeys = {}
dep_on = defaultdict(list)
inv_op = {'+': '-', '-': '+', '*': '/', '/': '*'}


def apply_monkey_values(initial_new_vals=None):
    global mvals, dep_on, monkeys
    new_vals = initial_new_vals if initial_new_vals else dict(mvals)
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

                    if isinstance(monkeys[depm]['a'], int) and isinstance(monkeys[depm]['b'], int) \
                            and monkeys[depm]['op'] != '=':
                        mv = int(eval("monkeys[depm]['a'] " + monkeys[depm]['op'] + " monkeys[depm]['b']"))
                        new_vals[depm] = mv
                        monkeys.pop(depm)

                dep_on.pop(mid)

        mvals |= new_vals


def resolve(m, val):
    if m == 'humn':
        return val

    a, op, b = monkeys[m]['a'], monkeys[m]['op'], monkeys[m]['b']
    if isinstance(a, int):
        if op in ['+', '*']:
            val = int(eval("val " + inv_op[op] + " a"))
        else:
            val = int(eval("a " + op + " val"))
        return resolve(b, val)
    else:
        val = int(eval("val " + inv_op[op] + " b"))
        return resolve(a, val)



def print_monkey_op(m):
    if isinstance(m, int):
        print(m, end=' ')
    elif m in mvals:
        print(mvals[m], end=' ')
        return
    elif m == 'humn':
        print('HUMN ', end='')
    else:
        mo = monkeys[m]
        print_monkey_op(mo['a'])
        print(mo['op'], end=' ')
        print_monkey_op(mo['b'])


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        mid, job = line.split(': ')
        if mid == 'humn':
            continue
        if re.match(r'\d+', job):
            mvals[mid] = int(job)
        else:
            a, op, b = job.split(' ')
            if 'humn' in (a, b):
                monkeys['humn'] = {'op': inv_op[op], 'a': (mid if a == 'humn' else a), 'b': (mid if b == 'humn' else b)}

            if mid == 'root': op = '='
            monkeys[mid] = {'op': op, 'a': a, 'b': b}
            dep_on[a].append(mid)
            dep_on[b].append(mid)

apply_monkey_values()
rm = monkeys['root']
if isinstance(rm['b'], int):
    mvals[rm['a']] = rm['b']
    print(resolve(rm['a'], mvals[rm['a']]))
else:
    mvals[rm['b']] = rm['a']
    print(resolve(rm['b'], mvals[rm['b']]))

print(datetime.datetime.now() - begin_time)
