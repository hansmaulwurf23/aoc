import datetime
import re

begin_time = datetime.datetime.now()

valves = {}
FLOW, TARGETS = range(2)
TIME_LEFT = 30

def max_flow(start):
    states = [(start, frozenset(), 0)]
    best_pressures = {}
    minutes_left = TIME_LEFT

    while minutes_left:
        #print(f'{len(states)} {len(best_pressures)}')
        minutes_left -= 1
        next_states = []
        for cur_valve, open_valves, press in states:
            if (cur_valve, open_valves) in best_pressures and press <= best_pressures[(cur_valve, open_valves)]:
                continue

            best_pressures[(cur_valve, open_valves)] = press

            if cur_valve not in open_valves and valves[cur_valve][FLOW]:
                next_states.append((cur_valve, frozenset(open_valves | {cur_valve}), press + valves[cur_valve][FLOW] * minutes_left))
            for dest in valves[cur_valve][TARGETS]:
                next_states.append((dest, open_valves, press))

        states = next_states

    return max(best_pressures.values())


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        valve, flow, targets = re.match(r'Valve (..) has flow rate=(\d+); tunnel[a-z]? lead[a-z]? to valve[a-z]? (.*)', line).groups()
        valves[valve] = (int(flow), targets.split(', '))

print(max_flow('AA'))
print(datetime.datetime.now() - begin_time)
