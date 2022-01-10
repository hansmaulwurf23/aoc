import datetime
begin_time = datetime.datetime.now()

activeCubes = set()

with open('./input.txt') as file:
    y = 0
    z = 0
    while line := file.readline().rstrip():
        for x in [i for i, p in enumerate(list(line)) if p == '#']:
            activeCubes.add((x, y, z))
        y += 1


def getCycleBounds(cubes):
    (fx, tx, fy, ty, fz, tz) = [None]*6
    for c in cubes:
        if fx is None or fx > c[0]: fx = c[0]
        if tx is None or tx < c[0]: tx = c[0]
        if fy is None or fy > c[1]: fy = c[1]
        if ty is None or ty < c[1]: ty = c[1]
        if fz is None or fz > c[2]: fz = c[2]
        # if tz is None or tz < c[2]: tz = c[2]
    return tuple([fx - 1, tx + 1, fy - 1, ty + 1, fz - 1])


def adjacents(x, y, z):
    return [(x+i,y+j,z+k) for i in range(-1, 2) for j in range(-1, 2) for k in range(-1, 2) if abs(i)+abs(j)+abs(k) != 0]


def cycle(activeCubes):
    (fx, tx, fy, ty, fz) = getCycleBounds(activeCubes)
    newActiveCubes = set()
    # loop non positive z only since everything is mirrored on the z = 0 plane
    for (x, y, z) in [(x, y, z) for x in range(fx, tx+1) for y in range(fy, ty+1) for z in range(fz, 1)]:
        iAmActive = ((x, y, z) in activeCubes)
        activeNeighbors = len([i for i in adjacents(x, y, z) if i in activeCubes])
        if (2 <= activeNeighbors <= 3 and iAmActive) or (activeNeighbors == 3 and not iAmActive):
            newActiveCubes.add((x, y, z))
            if (z != 0):
                newActiveCubes.add((x, y, -z))

    print(f'now there are {len(newActiveCubes)} active cubes')
    return newActiveCubes

for i in range(6):
    activeCubes = cycle(activeCubes)

print(len(activeCubes))
print(datetime.datetime.now() - begin_time)
