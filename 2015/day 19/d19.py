import datetime
import functools
import time
from collections import defaultdict, deque
import re

begin_time = datetime.datetime.now()

reactions = defaultdict(list)
molecule = None
with open('./input.txt') as f:
    lines = [line.rstrip() for line in f.readlines()]
    for line in lines[:-2]:
        f, t = line.split(' => ')
        reactions[f].append(t)

    molecule = lines[-1]

# reverse reaction are bijective
revreactions = dict()
for s, ts in reactions.items():
    for t in ts:
        revreactions[t] = s


def gen_graph(d: dict):
    n = dict()
    for k, v in d.items():
        if len(k) == 1:
            n[k] = v
            continue

        if k[0] not in n:
            n[k[0]] = dict()
        n[k[0]][k[1:]] = v

    for k, v in n.items():
        if isinstance(v, dict):
            n[k] = gen_graph(v)
    return n


revs = gen_graph(revreactions)
print(revs)

print(molecule)
print(pattern := f'[{"".join(revs.keys())}][^{"".join(revs.keys())}]*')
rest_mol = molecule
# while False:
#     parts = []
#     for sub in re.finditer(pattern, rest_mol):
#         prt = sub.group(0)
#         if prt in revreactions:
#             parts.append(revreactions[prt])
#         else:
#             parts.append(prt)
#
#     rest_mol = ''.join(parts)

root_nodes = 0
for source, targets in reactions.items():
    for target in targets:
        if molecule.find(target) >= 0:
            root_nodes += 1

def run_reactions(molecule, reactions):
    new_moles = set()
    i = 0
    for i, c in enumerate(molecule):
        if c in reactions:
            for n in reactions[c]:
                new_moles.add(molecule[:i] + n + molecule[i + 1:])

    for i, c in enumerate([molecule[x:x + 2] for x in range(len(molecule) - 1)]):
        if c in reactions:
            for n in reactions[c]:
                new_moles.add(molecule[:i] + n + molecule[i + 2:])

    return new_moles


rev_seen = set()
cur_min = None
visited_root_nodes = 0
cache = dict()

@functools.cache
def reverse(molecule: str, steps: int):
    global reactions, cur_min, root_nodes, visited_root_nodes, cache
    if molecule == 'e':
        print(f'new finished: {steps} after {datetime.datetime.now() - begin_time}')
        if cur_min is None or steps < cur_min:
            cur_min = steps
        return steps

    if steps == 1:
        visited_root_nodes += 1
        print(f'{visited_root_nodes}/{root_nodes} after {datetime.datetime.now() - begin_time}')

    l = len(molecule)
    if cur_min is not None and steps + (l // 10) > cur_min:
        return

    if molecule in cache and cache[molecule] <= steps:
        return
    cache[molecule] = steps

    # if l not in rev_seen:
    #     print(l, steps, molecule)
    #     rev_seen.add(l)

    min_steps = None
    subs = []
    for source, targets in reactions.items():
        for target in targets:
            if molecule.find(target) < 0:
                continue
            subs.append((target, source))

    subs = sorted(subs, key=lambda x: len(x[0]), reverse=True)
    for target, source in subs:
        s = reverse(molecule.replace(target, source, 1), steps + 1)
        if min_steps is None or (s is not None and s < min_steps):
            min_steps = s

        # idx = -1
        # while (idx := molecule.find(target, idx + 1)) >= 0:
        #     s = reverse(molecule[:idx] + molecule[idx:].replace(target, source, 1), steps + 1)
        #     if min_steps is None or (s is not None and s < min_steps):
        #         min_steps = s

    return min_steps


@functools.cache
def reverse_reactions(molecule: str):
    global reactions
    if molecule == 'e':
        return []

    new_moles = []
    for source, targets in reactions.items():
        for target in targets:
            if molecule.find(target) < 0:
                continue

            new_moles.append(molecule.replace(target, source))
            idx = -1
            while (idx := molecule.find(target, idx + 1)) >= 0:
                new_moles.append(molecule[:idx] + molecule[idx:].replace(target, source, 1))

    return new_moles


def bfs(start, end):
    global reactions
    q = deque()
    q.append((start, 0))
    seen = set()
    elen = len(end)
    while q:
        cur_mol, steps = q.popleft()

        if steps not in rev_seen:
            print(steps, len(cur_mol), cur_mol)
            rev_seen.add(steps)

        if cur_mol == end:
            return steps

        # for new_mol in reverse_reactions(cur_mol):
        for new_mol in run_reactions(cur_mol, reactions):
            if new_mol not in seen:
                q.append((new_mol, steps + 1))
                seen.add(new_mol)


print(f'part1: {len(run_reactions(molecule, reactions))}')
# print(f'part2: {bfs("e", molecule)}')
# print(bfs(molecule, 'e'))
print(reverse(molecule, 0))
print('82 wrong.')
print('39 wrong.')
print('38 wrong.')
print(datetime.datetime.now() - begin_time)
