import datetime
import functools
from collections import defaultdict, deque

begin_time = datetime.datetime.now()
graph = defaultdict(list)


def dfs1(node, end, seen):
    global graph

    if node == end:
        return 1

    if node.islower():
        seen |= {node}

    return sum([dfs1(nxt, end, set() | seen) for nxt in graph[node] if nxt not in seen])


@functools.cache
def dfs2(node, end, sc, seen):
    global graph

    if node == end:
        return 1

    if node.islower():
        seen |= {node}

    return sum([dfs2(n, end, n if n in seen else sc, frozenset(set() | seen)) for n in graph[node] if
                n not in seen or sc is None])


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        src, dst = line.split('-')
        src, dst = (dst, src) if dst == 'start' else (src, dst)
        src, dst = (dst, src) if src == 'end' else (src, dst)
        graph[src].append(dst)
        if src != 'start':
            graph[dst].append(src)

print(f'part 1: {dfs1('start', 'end', set())}')
print(f'part 2: {dfs2('start', 'end', None, frozenset())}')
print(datetime.datetime.now() - begin_time)
print(dfs2.cache_info())
