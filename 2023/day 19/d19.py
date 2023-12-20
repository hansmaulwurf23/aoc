import datetime
from collections import defaultdict
from copy import deepcopy
from functools import partial, reduce

from aopython import intersect_ranges

begin_time = datetime.datetime.now()

gt = lambda n, v, r: r if n > v else False
lt = lambda n, v, r: r if n < v else False
tr = lambda n, r: r

INVERSE = {'>': '<=', '<': '>='}

def parse_parts(raw: str):
    parts = []
    for lp in [l[1:-1].split(',') for l in raw.splitlines()]:
        parts.append({k: int(v) for k, v in [x.split('=') for x in lp]})
    return parts

def parse_workflows(raw: str):
    workflows = {}
    for l in raw.splitlines():
        name, defs = l[:-1].split('{')
        defs = defs.split(',')
        conds = []
        for d in defs:
            (cond, target) = d.split(':') if ':' in d else (None, d)
            if cond is None:
                conds.append((None, partial(tr, r=target)))
            elif '>' in cond:
                n, v = cond.split('>')
                conds.append((n, partial(gt, r=target, v=int(v))))
            elif '<' in cond:
                n, v = cond.split('<')
                conds.append((n, partial(lt, r=target, v=int(v))))
            else:
                raise RuntimeError(f'Unknown condition {cond}')

        workflows[name] = conds
    return workflows

def eval_parts(parts):
    tot = 0
    for part in parts:
        cw = 'in'
        while True:
            for conds in workflows[cw]:
                if nf := conds[1](part[conds[0]] if conds[0] else 42):
                    cw = nf
                    break

            if cw == 'R':
                break
            elif cw == 'A':
                tot += sum(part.values())
                break
    return tot

def count_configs(raw:str):
    workflows = defaultdict(list)
    for l in raw.splitlines():
        name, defs = l[:-1].split('{')
        defs = defs.split(',')
        for d in defs:
            (cond, target) = d.split(':') if ':' in d else (None, d)
            if cond is None:
                workflows[name].append((cond, target))
            else:
                op, n, val = (['<'] + cond.split('<') if '<' in cond else ['>'] + cond.split('>'))
                workflows[name].append(([n, op, int(val)], target))

    def find_all_configs(cw:str, current_conds):
        all_comb = []
        inverses = []
        for conditions in workflows[cw]:
            cond, target = conditions
            if target == 'A':
                all_comb.append(current_conds + inverses + ([cond] if cond is not None else []))
            elif target != 'R':
                all_comb.extend(find_all_configs(target, current_conds + inverses + ([cond] if cond is not None else [])))
            if cond is not None:
                inverses.append([cond[0], INVERSE[cond[1]], cond[2]])
        return all_comb

    def infer_range(op, val):
        match op:
            case '<':
                return range(1, val)
            case '<=':
                return range(1, val + 1)
            case '>':
                return range(val+1, 4001)
            case '>=':
                return range(val, 4001)

    configs = find_all_configs('in', [])
    tot = 0
    start = {'x': range(1, 4001), 'm': range(1, 4001), 'a': range(1, 4001), 's': range(1, 4001)}
    for config in configs:
        rest = deepcopy(start)
        for n, op, val in config:
            r = infer_range(op, val)
            rest[n] = intersect_ranges(rest[n], r)
        tot += reduce(lambda a, b: a * b, map(len, rest.values()))
    return tot

with open('./input.txt') as f:
    raw_wfs, raw_parts = f.read().split('\n\n')
    workflows = parse_workflows(raw_wfs)
    parts = parse_parts(raw_parts)

p1 = eval_parts(parts)
print(f'part 1: {p1}')
assert p1 in [406934, 19114]
p2 = count_configs(raw_wfs)
print(f'part 2: {p2}')
assert p2 in [131192538505367, 167409079868000]
print(datetime.datetime.now() - begin_time)
