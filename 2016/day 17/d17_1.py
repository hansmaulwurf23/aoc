import datetime
from collections import deque
from hashlib import md5

from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
MAP_SIZE = 4


def adjacents(path, passcode):
    global DIRS
    adjas = []
    hash = md5(f'{passcode}{path}'.encode()).hexdigest()[:4]
    for k, h in zip(DIRS.keys(), hash):
        if h >= 'b':
            adjas.append(k)

    return adjas


def bfs(start, end, passcode):
    q = deque([(start, '')])
    while q:
        cur_pos, path = q.popleft()

        if cur_pos == end:
            return path

        for a in adjacents(path, passcode):
            new_pos = tuple(vector_add(cur_pos, DIRS[a]))
            if 0 <= new_pos[0] < MAP_SIZE and 0 <= new_pos[1] < MAP_SIZE:
                q.append((new_pos, path + a))


print(bfs((0, 0), (MAP_SIZE - 1, MAP_SIZE - 1), 'veumntbg'))
# print(bfs((0, 0), (3, 3), 'ihgpwlah'))
print(datetime.datetime.now() - begin_time)
