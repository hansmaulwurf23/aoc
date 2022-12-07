import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()
dir_sizes = defaultdict(lambda: 0)
disk_size = 70000000
update_size = 30000000

with open('./input.txt') as f:
    cwd = ()
    while line := f.readline().rstrip():
        if line[0] == '$':
            cmd = line[2:]
            if cmd[0:2] == 'cd':
                cd = cmd.split(' ')[-1]
                if cd == '/':
                    cwd = ()
                elif cd == '..':
                    cwd = cwd[:-1]
                else:
                    cwd = cwd + (cd,)
        elif line[0:3] == 'dir':
            pass
        else:
            size = int(line.split(' ')[0])
            dir_sizes[cwd] += size
            if cwd != ():
                parent = tuple(cwd)
                while parent := parent[:-1]:
                    dir_sizes[parent] += size
                dir_sizes[()] += size

print(f'sum of small dirs: {sum(filter(lambda x: x <= 100000, dir_sizes.values()))}')

cur_free = disk_size - dir_sizes[()]
min_free = update_size - cur_free
print(f'min dir to delete: {min(filter(lambda x: x >= min_free, dir_sizes.values()))}')

print(datetime.datetime.now() - begin_time)
