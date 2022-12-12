import datetime
import math

begin_time = datetime.datetime.now()

monkeys = [{'inspect_counter': 0}]


def play_round():
    for monkey in monkeys:
        items = monkey['items']
        monkey['items'] = []
        for item in items:
            monkey['inspect_counter'] += 1
            wl = monkey['new'](item)
            wl = wl % limit_modulo
            if wl % monkey['divisible'] == 0:
                monkeys[monkey['true_monkey']]['items'].append(wl)
            else:
                monkeys[monkey['false_monkey']]['items'].append(wl)


limit_modulo = 1
with open('./input.txt') as f:
    lines = f.readlines()
    idx = 0
    for line in lines:
        line = line.rstrip()
        if not line.rstrip():
            monkeys.append({'inspect_counter': 0})
            idx += 1
        elif line.startswith('  Starting items:'):
            monkeys[-1]['items'] = list(map(int, line[18:].split(', ')))
        elif line.startswith('  Operation: '):
            operator, operand = line[23:].split(' ')
            if operator == '+':
                if operand == 'old':
                    monkeys[-1]['new'] = lambda old: old + old
                else:
                    operand = int(operand)
                    monkeys[-1]['new'] = lambda old, o=operand: old + o
            elif operator == '*':
                if operand == 'old':
                    monkeys[-1]['new'] = lambda old: old * old
                else:
                    operand = int(operand)
                    monkeys[-1]['new'] = lambda old, o=operand: old * o

        elif line.startswith('  Test: divisible by '):
            monkeys[-1]['divisible'] = int(line[21:])
            limit_modulo *= monkeys[-1]['divisible']
        elif line.startswith('    If true: throw to monkey '):
            monkeys[-1]['true_monkey'] = int(line[29:])
        elif line.startswith('    If false: throw to monkey '):
            monkeys[-1]['false_monkey'] = int(line[30:])

for r in range(10000):
    play_round()

most_active = list(sorted((m['inspect_counter'] for m in monkeys), reverse=True))[0:2]
print(f'monkey business: {math.prod(most_active)}')
print(datetime.datetime.now() - begin_time)
