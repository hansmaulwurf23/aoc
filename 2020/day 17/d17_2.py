import datetime
begin_time = datetime.datetime.now()

activeCubes = set()

with open('./input.txt') as file:
    y = 0
    (z, w) = [0]*2
    while line := file.readline().rstrip():
        for x in [i for i, p in enumerate(list(line)) if p == '#']:
            activeCubes.add((x, y, z, w))
        y += 1


def getCycleBounds(cubes):
    """
    Cycles thru all cubes to get minimum x, y, z, w and maximum x, y coordinates offset by one into the dimension
    """
    (fx, tx, fy, ty, fz, fw) = [None]*6
    for c in cubes:
        if fx is None or fx > c[0]: fx = c[0]
        if tx is None or tx < c[0]: tx = c[0]
        if fy is None or fy > c[1]: fy = c[1]
        if ty is None or ty < c[1]: ty = c[1]
        if fz is None or fz > c[2]: fz = c[2]
        # if tz is None or tz < c[2]: tz = c[2]
        if fw is None or fw > c[3]: fw = c[3]
        # if tw is None or tw < c[3]: tw = c[3]
    return fx - 1, tx + 1, fy - 1, ty + 1, fz - 1, fw - 1


def adjacents(x, y, z, w):
    return [(x+i,y+j,z+k,w+l)
            for i in range(-1, 2)
            for j in range(-1, 2)
            for k in range(-1, 2)
            for l in range(-1, 2)
            if abs(i)+abs(j)+abs(k)+abs(l) != 0]


def cycle(activeCubes):
    (fx, tx, fy, ty, fz, fw) = getCycleBounds(activeCubes)
    newActiveCubes = set()
    # loop non positive z and w only since everything is mirrored on the z = 0 and w = 0 plane
    for (x, y, z, w) in [(x, y, z, w) for x in range(fx, tx+1) for y in range(fy, ty+1) for z in range(fz, 1) for w in range(fw, 1)]:
        iAmActive = ((x, y, z, w) in activeCubes)
        activeNeighbors = len([i for i in adjacents(x, y, z, w) if i in activeCubes])
        if (2 <= activeNeighbors <= 3 and iAmActive) or (activeNeighbors == 3 and not iAmActive):
            newActiveCubes.add((x, y, z, w))
            if z != 0:
                newActiveCubes.add((x, y, -z, w))
            if w != 0:
                newActiveCubes.add((x, y, z, -w))
            if w != 0 and z != 0:
                newActiveCubes.add((x, y, -z, -w))


    print(f'now there are {len(newActiveCubes)} active cubes')
    return newActiveCubes

for i in range(6):
    activeCubes = cycle(activeCubes)

print(len(activeCubes))
print(datetime.datetime.now() - begin_time)
