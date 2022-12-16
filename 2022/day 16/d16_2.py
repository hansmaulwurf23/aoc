import datetime
import re
from collections import defaultdict
import functools

begin_time = datetime.datetime.now()

TIME_LEFT = 26
valves = set()
graph = defaultdict(lambda: 1000000)
flows = {}
root = 'AA'


def floyd_warshall():
    for x, y, z in [(x, y, z) for x in valves for y in valves for z in valves]:
        graph[y, z] = min(graph[y, z], graph[y, x] + graph[x, z])


@functools.cache
def search(minutes_left, cur_valve, valves_left, elephant):
    max_press = 0
    # only examine left valves that can be reached in time
    for next_valve in [v for v in valves_left if graph[cur_valve, v] < minutes_left]:
        # open this valve
        press = flows[next_valve] * (minutes_left - graph[cur_valve, next_valve] - 1)
        # and continue dfs
        press += search(minutes_left - graph[cur_valve, next_valve] - 1, next_valve, valves_left - {next_valve}, elephant)
        max_press = max(press, max_press)

    # run dfs for myself as well
    if elephant:
        press = search(26, root, valves_left, False)
        max_press = max(press, max_press)

    return max_press


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        valve, flow, targets = re.match(r'Valve (..) has flow rate=(\d+); tunnel[a-z]? lead[a-z]? to valve[a-z]? (.*)', line).groups()
        valves.add(valve)
        if v := int(flow):
            flows[valve] = v
        for target in targets.split(', '):
            graph[valve, target] = 1

# build the complete graph
floyd_warshall()
# run with flows as valves_left since all other valves are useless to reduce the pressure
print(search(TIME_LEFT, root, frozenset(flows), True))
# lol: this solution solves part one 3 times faster than my other implementation
# print(search(TIME_LEFT + 4, root, frozenset(flows), False))
print(datetime.datetime.now() - begin_time)
