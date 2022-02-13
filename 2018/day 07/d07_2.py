import copy
import datetime
import re
from collections import defaultdict
import heapq

begin_time = datetime.datetime.now()

NEXT, REQS = 0, 1
WORKER = 5


def calc_work_time(node):
    return 61 + ord(node) - ord('A')
    # return 1 + ord(node) - ord('A')


def run_workers(graph):
    res = []
    worker_queue = [[] for i in range(WORKER)]

    queue = []
    # find all steps, that have no requirements and put them in the ordered queue to start with
    for name, step in graph.items():
        if step[REQS] == 0:
            heapq.heappush(queue, name)

    seconds = 0
    while True:
        for w in worker_queue:
            if w:
                cur_node = w.pop()

                # still work to do? -> next worker
                if w:
                    continue

                res.append(cur_node)
                for neighbour in graph[cur_node][NEXT]:
                    graph[neighbour][REQS] -= 1

                    # no more requirements -> ready for work
                    if graph[neighbour][REQS] == 0:
                        heapq.heappush(queue, neighbour)

            if queue:
                cur_node = heapq.heappop(queue)
                w.extend([cur_node] * calc_work_time(cur_node))

        if not queue and sum(map(len, worker_queue)) == 0:
            break

        seconds += 1

    return res, seconds


graph = defaultdict(lambda: [set(), 0])
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        source, target = re.match(r'Step (.) must be finished before step (.) can begin.', line).groups()
        graph[source][NEXT].add(target)
        graph[target][NEXT].add(source)
        graph[target][REQS] += 1


order, secs = run_workers(graph)
print(''.join(order))
print(secs)
print(datetime.datetime.now() - begin_time)
