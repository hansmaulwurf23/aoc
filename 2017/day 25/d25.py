import datetime
import re

begin_time = datetime.datetime.now()
WRITE, MOVE, NEXT = range(3)
cur_state = None
blueprints = dict()

with open('./input.txt') as f:
    lines = f.readlines()
    cur_state = lines[0][-3]
    steps = int(re.findall(r'\d+', lines[1])[0])

    lno = 3
    while lno < len(lines):
        s = lines[lno][-3]
        blueprints[s] = [None, None]
        for i in range(2):
            val = [int(s) for s in re.findall(r'\d', lines[lno+1])][0]
            blueprints[s][val] = [0] * 3
            blueprints[s][val][WRITE] = [int(s) for s in re.findall(r'\d', lines[lno+2])][0]
            blueprints[s][val][MOVE] = 1 if re.findall(r'(right|left)', lines[lno+3])[0] == 'right' else -1
            blueprints[s][val][NEXT] = lines[lno+4][-3]
            lno += 4
        lno += 2

tlen = 10000
tape = [0] * tlen
cur_idx = tlen - (tlen // 4)
# tape = [0]
# cur_idx = 0
# tlen = 1
for step in range(steps):
# for step in range(100):
    val = tape[cur_idx]
    tape[cur_idx] = blueprints[cur_state][val][WRITE]
    cur_idx = cur_idx + blueprints[cur_state][val][MOVE]
    if cur_idx == tlen:
        tape.append(0)
        tlen += 1
    elif cur_idx == -1:
        tape.insert(0, 0)
        cur_idx = 0
        tlen += 1
    cur_state = blueprints[cur_state][val][NEXT]
    #print(' '.join(map(lambda i: f"[{tape[i]}]" if i == cur_idx else str(tape[i]), range(tlen))))

print(sum(tape))
print(datetime.datetime.now() - begin_time)
