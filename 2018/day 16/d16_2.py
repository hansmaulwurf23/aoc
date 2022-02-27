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

    return tests, i


def read_script(lines):
    instr = []
    for l in lines:
        instr.append(tuple(map(int, re.findall(r'\d+', l))))

    return instr

def run_script(script, op_codes):
    regs = [0, 0, 0, 0]
    for instr in script:
        raw_op, a, b, c = instr
        op = op_codes[raw_op]

        if op == ADDR:
            regs[c] = regs[a] + regs[b]
        elif op == ADDI:
            regs[c] = regs[a] + b
        elif op == MULR:
            regs[c] = regs[a] * regs[b]
        elif op == MULI:
            regs[c] = regs[a] * b
        elif op == BANR:
            regs[c] = regs[a] & regs[b]
        elif op == BANI:
            regs[c] = regs[a] & b
        elif op == BORR:
            regs[c] = regs[a] | regs[b]
        elif op == BORI:
            regs[c] = regs[a] | b
        elif op == SETR:
            regs[c] = regs[a]
        elif op == SETI:
            regs[c] = a
        elif op == GTIR:
            regs[c] = (1 if a > regs[b] else 0)
        elif op == GTRI:
            regs[c] = (1 if regs[a] > b else 0)
        elif op == GTRR:
            regs[c] = (1 if regs[a] > regs[b] else 0)
        elif op == EQIR:
            regs[c] = (1 if a == regs[b] else 0)
        elif op == EQRI:
            regs[c] = (1 if regs[a] == b else 0)
        elif op == EQRR:
            regs[c] = (1 if regs[a] == regs[b] else 0)

    return regs[0]

with open('./input.txt') as f:
    lines = f.readlines()

tests, lines_read = read_tests(lines)
script = read_script(lines[lines_read+2:])
op_codes = dict()
for op_code in range(16):
    op_codes[op_code] = set(range(16))

for t in tests:
    op_code = t[1][0]
    matches = set(test_instr(*t[0:3]))
    op_codes[op_code] &= matches
    # only one op code remains -> remove it from all others
    if len(op_codes[op_code]) == 1:
        for o in [o for o in op_codes.keys() if o != op_code]:
            op_codes[o] -= op_codes[op_code]

# replace op codes sets with single remaining op code
for o in op_codes.keys():
    op_codes[o] = op_codes[o].pop()

print(run_script(script, op_codes))
print(datetime.datetime.now() - begin_time)
