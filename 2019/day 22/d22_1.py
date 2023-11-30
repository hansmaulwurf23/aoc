import datetime
import re

begin_time = datetime.datetime.now()


def run_cmds(cmds, use_idx, no_cards):
    idx = use_idx

    for line in [l.rstrip() for l in cmds if l.rstrip()]:
        # print(line)
        if line == 'deal into new stack':
            idx = no_cards - idx - 1
        elif matches := re.match(r'cut ([-]*\d+)', line):
            val = int(matches.groups()[0])
            idx = idx - val % no_cards
        elif matches := re.match(r'deal with increment ([-]*\d+)', line):
            val = int(matches.groups()[0])
            idx = (idx * val) % no_cards
        else:
            print('read error.')

    return idx


with open('./input.txt') as f:
    cmds = f.readlines()

# no_cards = 10
# res = [0] * 10
# for i in range(no_cards):
#     res[run_cmds(cmds, i, no_cards)] = i
# print(' '.join(map(str, res)))

no_cards = 10007
print(run_cmds(cmds, 2019, no_cards))
print(datetime.datetime.now() - begin_time)
