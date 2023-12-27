import sympy

hailstones = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        pos, v = line.split(' @ ')
        hailstones.append([list(map(int, pos.split(', '))), list(map(int, v.split(', ')))])

rx, ry, rz, vrx, vry, vrz = sympy.symbols("rx, ry, rz, vrx, vry, vrz")

equations = []

for i, ((x, y, z), (vx, vy, vz)) in enumerate(hailstones):
    equations.append((rx - x) * (vy - vry) - (ry - y) * (vx - vrx))
    equations.append((ry - y) * (vz - vrz) - (rz - z) * (vy - vry))
    if i >= 2:
        solutions = [soln for soln in sympy.solve(equations) if all(x % 1 == 0 for x in soln.values())]
        if len(solutions) == 1:
            break

rp = solutions[0]

print(rp[rx] + rp[ry] + rp[rz])
