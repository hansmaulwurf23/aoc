import datetime
import functools
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

MAX = 65535
formulas = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        expression, target = line.split(' -> ')
        formulas[target] = expression

@functools.cache
def evaluate(var):
    global formulas

    if var not in formulas:
        return int(var)

    expr = formulas[var]
    if expr.isnumeric():
        return int(expr)
    parts = expr.split(' ')
    if len(parts) == 1:
        return evaluate(expr)
    if len(parts) == 2:
        op, oper = parts
        if op == 'NOT':
            return MAX ^ evaluate(oper)
        else:
            print(f'ERROR unknow op {op} in {expr}')
    elif len(parts) == 3:
        a, op, b = parts
        if op == 'RSHIFT':
            return evaluate(a) >> int(b)
        elif op == 'LSHIFT':
            return evaluate(a) << int(b)
        elif op == 'AND':
            return evaluate(a) & evaluate(b)
        elif op == 'OR':
            return evaluate(a) | evaluate(b)
        else:
            print(f'ERROR unknown op {op} in {expr}')
    else:
        print(f'WTF {expr}')


res1 = evaluate("a")
print(f'part 1 {res1}')
print(evaluate.cache_info())
formulas['b'] = f'{res1}'
evaluate.cache_clear()
print(f'part 2 {evaluate("a")}')
print(datetime.datetime.now() - begin_time)
