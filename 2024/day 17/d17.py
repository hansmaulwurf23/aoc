import datetime
begin_time = datetime.datetime.now()
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = range(8)


def combo(regs, val):
    if val == 7: return None
    return val if val <= 3 else regs[chr(ord('A') + val - 4)]


def run(prg, regs, only_first_out = False):
    outputs = []
    ip = 0
    while ip < len(prg):
        op, oper = prg[ip], prg[ip+1]
        cbop = combo(regs, oper)

        if op == ADV:
            regs['A'] //= (2**cbop)
        elif op == BXL:
            regs['B'] = regs['B'] ^ oper
        elif op == BST:
            regs['B'] = cbop & 7
        elif op == JNZ:
            if regs['A']:
                ip = oper
                continue
        elif op == BXC:
            regs['B'] ^= regs['C']
        elif op == OUT:
            if only_first_out:
                return cbop & 7
            outputs.append(cbop & 7)
        elif op == BDV:
            regs['B'] = regs['A'] // (2 ** cbop)
        elif op == CDV:
            regs['C'] = regs['A'] // (2 ** cbop)

        ip += 2

    return outputs


regs = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        r, v = line.replace('Register ', '').split(': ')
        regs[r] = int(v)

    prg = list(map(int, f.readline().rstrip().replace('Program: ', '').split(',')))

# regs, prg, assertion = {'A': 0, 'B': 0, 'C': 9}, [2, 6], "regs['B'] == 1"
# regs, prg, assertion = {'A': 10, 'B': 0, 'C': 0}, [5, 0, 5, 1, 5, 4], 'p1 == [0,1,2]'
# regs, prg, assertion = {'A': 2024, 'B': 0, 'C': 0}, [0, 1, 5, 4, 3, 0], 'p1 == [4,2,5,6,7,7,7,7,3,1,0]'
# regs, prg, assertion = {'A': 0, 'B': 29, 'C': 0}, [1, 7], "regs['B'] == 26"
# regs, prg, assertion = {'A': 0, 'B': 2024, 'C': 43690}, [4, 0], "regs['B'] == 44354"
assertion = 'p1 == [7,4,2,5,1,4,6,0,4]'

p1 = run(prg, regs)
print(f'part 1: {','.join(map(str, p1))}')
if assertion:  assert eval(assertion)

# terminating condition!
valids = {0}
# beginning from the end add one more output at a time
for subprg in [prg[-l:] for l in range(1, len(prg)+1)]:
    new_valids = set()
    for a in [a << 3 for a in valids]:
        new_valids |= {a | lst3bits for lst3bits in range(8) \
                       if run(prg, {'A': a | lst3bits, 'B': 0, 'C': 0}, only_first_out=True) == subprg[0]}
    valids = new_valids

p2 = min(valids)
print(f'part 2: {p2}')
assert p2 in (164278764924605,)
print(datetime.datetime.now() - begin_time)
