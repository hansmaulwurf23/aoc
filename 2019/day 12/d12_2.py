import datetime
from functools import reduce
from itertools import combinations
from aopython import lcm

begin_time = datetime.datetime.now()

moon_positions = []
moon_velocities = []


def orbit(positions, velocities):
    org_positions = tuple(positions)
    org_velocities = tuple(velocities)
    steps = 0

    while True:
        # apply gravity
        for i, o in combinations(range(4), 2):
            if positions[o] > positions[i]:
                velocities[i] += 1
                velocities[o] -= 1
            elif positions[o] < positions[i]:
                velocities[i] -= 1
                velocities[o] += 1

        # apply velocity
        for i in range(4):
            positions[i] = positions[i] + velocities[i]

        steps += 1

        if org_velocities == tuple(velocities):
            if org_positions == tuple(positions):
                break

    return steps


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        moon_positions.append(list([int(l[2:]) for l in line[1:-1].split(', ')]))
        moon_velocities.append([0] * 3)

all_steps = []
for dim in range(3):
    all_steps.append(orbit([p[dim] for p in moon_positions], [v[dim] for v in moon_velocities]))

print(all_steps)
steps = reduce(lcm, all_steps, 1)
print(steps)
print(datetime.datetime.now() - begin_time)
