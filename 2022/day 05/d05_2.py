import datetime
import re

begin_time = datetime.datetime.now()
stacks = []
with open('./input.txt') as f:
    stacks_raw = []
    while line := f.readline().rstrip():
        if line.find('[') >= 0:
            stacks_raw.append(line)
        else:
            max_stack_id = int(re.findall(r'(\d+)', line)[-1])
            for i in range(max_stack_id + 1):
                stacks.append([])

    # parse stacks
    for s in reversed(stacks_raw):
        for i in range(max_stack_id):
            if len(s) < 1 + i * 4:
                break
            v = s[1 + i * 4]
            if v != ' ':
                stacks[i+1].append(v)

    # run commands
    while line := f.readline().rstrip():
        vol, src, dst = map(int, re.findall(r'\d+', line))
        stacks[dst].extend(stacks[src][-vol:])
        stacks[src][-vol:] = []

    for i in range(max_stack_id):
        print(stacks[i+1][-1], end='')
    print('')
print(datetime.datetime.now() - begin_time)
