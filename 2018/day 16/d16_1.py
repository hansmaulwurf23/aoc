import datetime
import re

begin_time = datetime.datetime.now()

ADDR, ADDI, MULR, MULI, BANR, BANI, BORR, BORI, SETR, SETI, GTIR, GTRI, GTRR, EQIR, EQRI, EQRR = range(16)


def test_instr(bregs, instr, aregs):
    op, a, b, c = instr
    matches = []

    if aregs[c] == bregs[a] + bregs[b]:
        matches.append(ADDR)

    if aregs[c] == bregs[a] + b:
        matches.append(ADDI)

    if aregs[c] == bregs[a] * bregs[b]:
        matches.append(MULR)

    if aregs[c] == bregs[a] * b:
        matches.append(MULI)

    if aregs[c] == bregs[a] & bregs[b]:
        matches.append(BANR)

    if aregs[c] == bregs[a] & b:
        matches.append(BANI)

    if aregs[c] == bregs[a] | bregs[b]:
        matches.append(BORR)

    if aregs[c] == bregs[a] | b:
        matches.append(BORI)

    if aregs[c] == bregs[a]:
        matches.append(SETR)

    if aregs[c] == a:
        matches.append(SETI)

    if aregs[c] == (1 if a > bregs[b] else 0):
        matches.append(GTIR)

    if aregs[c] == (1 if bregs[a] > b else 0):
        matches.append(GTRI)

    if aregs[c] == (1 if bregs[a] > bregs[b] else 0):
        matches.append(GTRR)

    if aregs[c] == (1 if a == bregs[b] else 0):
        matches.append(EQIR)

    if aregs[c] == (1 if bregs[a] == b else 0):
        matches.append(EQRI)

    if aregs[c] == (1 if bregs[a] == bregs[b] else 0):
        matches.append(EQRR)

    return matches


def read_tests(lines):
    tests = []
    for i in range(0, len(lines), 4):
        if lines[i].startswith('Before'):
            bregs = tuple(map(int, re.findall(r'\d+', lines[i])))
            instr = tuple(map(int, re.findall(r'\d+', lines[i + 1])))
            aregs = tuple(map(int, re.findall(r'\d+', lines[i + 2])))
            tests.append((bregs, instr, aregs))
        else:
            break

    return tests


with open('./input.txt') as f:
    lines = f.readlines()

right = 0
tests = read_tests(lines)
for t in tests:
    if len(test_instr(*t[0:3])) >= 3:
        right += 1

print(right)
print(datetime.datetime.now() - begin_time)
