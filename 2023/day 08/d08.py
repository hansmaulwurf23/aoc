import datetime
import re
from functools import reduce
from aopython import lcm

begin_time = datetime.datetime.now()

MOVES = {'L': 0, 'R': 1}
graph = dict()
with open('./input.txt') as f:
    lines = f.read().splitlines()

commands = list(lines[0])
cmd_count = len(commands)
for line in lines[2:]:
    node, left, right = re.findall(r'[A-Z]{3}', line)
    graph[node] = (left, right)

node, cmd, steps = 'AAA', 0, 0
while node != 'ZZZ':
    steps += 1
    node = graph[node][MOVES[commands[cmd]]]
    cmd = (cmd + 1) % cmd_count

print(f'part 1: {steps}')

current_nodes = [n for n in graph.keys() if n[-1] == 'A']
node_steps = []
for node in current_nodes:
    cmd, steps = 0, 0
    while node[-1] != 'Z':
        steps += 1
        node = graph[node][MOVES[commands[cmd]]]
        cmd = (cmd + 1) % cmd_count
    node_steps.append(steps)

print(f'part 2: {reduce(lambda x, y: lcm(x, y), node_steps)}')
print(datetime.datetime.now() - begin_time)
