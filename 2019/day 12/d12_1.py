import datetime
from aopython import vector_sgn, vector_abs

begin_time = datetime.datetime.now()

moon_positions = []
moon_velocities = []


def step(moon_positions, moon_velocities):
    # apply gravity
    vel_deltas = [[0] * 3] * 4
    for i in range(4):
        for o in range(i+1, 4):
            v = (moon_positions[o][0] - moon_positions[i][0],
                 moon_positions[o][1] - moon_positions[i][1],
                 moon_positions[o][2] - moon_positions[i][2])

            gravity_vector = vector_sgn(v)

            vel_deltas[i] = (vel_deltas[i][0] + gravity_vector[0],
                             vel_deltas[i][1] + gravity_vector[1],
                             vel_deltas[i][2] + gravity_vector[2])

            inv = (-gravity_vector[0], -gravity_vector[1], -gravity_vector[2])
            vel_deltas[o] = (vel_deltas[o][0] + inv[0],
                             vel_deltas[o][1] + inv[1],
                             vel_deltas[o][2] + inv[2])

        moon_velocities[i] = (moon_velocities[i][0] + vel_deltas[i][0],
                              moon_velocities[i][1] + vel_deltas[i][1],
                              moon_velocities[i][2] + vel_deltas[i][2])

    # apply velocity
    for i in range(4):
        moon_positions[i] = (moon_positions[i][0] + moon_velocities[i][0],
                             moon_positions[i][1] + moon_velocities[i][1],
                             moon_positions[i][2] + moon_velocities[i][2])


def calc_system_energy(moon_positions, moon_velocities):
    energy = 0
    for p, v in zip(moon_positions, moon_velocities):
        energy += (sum(vector_abs(p)) * sum(vector_abs(v)))
    return energy


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        moon_positions.append(list([int(l[2:]) for l in line[1:-1].split(', ')]))
        moon_velocities.append([0] * 3)

for i in range(1000):
    step(moon_positions, moon_velocities)


print(calc_system_energy(moon_positions, moon_velocities))
print(datetime.datetime.now() - begin_time)
