import datetime
begin_time = datetime.datetime.now()

orbits = dict()
with open('./input.txt') as f:
    while line  := f.readline().rstrip():
        center, orbiter = line.split(')')
        orbits[orbiter] = center


def get_path_to_com(orbits, start, path):
    path.append(start)
    if start == 'COM':
        return path
    else:
        return get_path_to_com(orbits, orbits[start], path)

# get paths to COM
my_path = get_path_to_com(orbits, 'YOU', [])
santas_path = get_path_to_com(orbits, 'SAN', [])
# lengths of paths - twice length of same path - 2 (since "Between the objects they are orbiting - not between YOU and SAN.")
print(len(my_path) + len(santas_path) - 2 * len(set(my_path) & set(santas_path)) - 2)
print(datetime.datetime.now() - begin_time)
