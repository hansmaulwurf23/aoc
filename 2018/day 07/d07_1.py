import copy
import datetime
import re
from collections import defaultdict
import heapq

begin_time = datetime.datetime.now()

NEXT, REQS = 0, 1


def topological_sort(graph):
    res = []

    queue = []
    # find all steps, that have no requirements and put them in the ordered queue to start with
    for name, step in graph.items():
        if step[REQS] == 0:
            heapq.heappush(queue, name)

    while queue:
        cur_node = heapq.heappop(queue)
        res.append(cur_node)

        for neighbour in graph[cur_node][NEXT]:
            graph[neighbour][REQS] -= 1

            # no more requirements -> ready for alphabetical sorting
            if graph[neighbour][REQS] == 0:
                heapq.heappush(queue, neighbour)

    return res


graph = defaultdict(lambda: [set(), 0])
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        source, target = re.match(r'Step (.) must be finished before step (.) can begin.', line).groups()
        graph[source][NEXT].add(target)
        graph[target][NEXT].add(source)
        graph[target][REQS] += 1


order = topological_sort(graph)
print(''.join(order))
print(datetime.datetime.now() - begin_time)
