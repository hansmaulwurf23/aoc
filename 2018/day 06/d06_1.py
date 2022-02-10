import datetime
from collections import defaultdict, Counter

import showgrid
from aopython import min_max_2d, vector_add, manhattan_distance
begin_time = datetime.datetime.now()


def process(locations):
    fx, tx, fy, ty = min_max_2d(locations)
    edge_ids = {-1}
    heatmap = []
    for x, y in [(x, y) for x in range(fx, tx + 1) for y in range(fy, ty + 1)]:
        distances = defaultdict(lambda: [])
        cur_min = None
        for id, l in enumerate(locations):
            distance = manhattan_distance(l, (x, y))
            if cur_min is not None and distance < cur_min:
                cur_min = distance
            distances[distance].append(id)

        min_dist = min(distances.keys())
        if len(distances[min_dist]) == 1:
            heatmap.append((x, y, distances[min_dist][0]))
            if x == fx or y == fy or x == tx or y == ty:
                edge_ids.add(distances[min_dist][0])
        else:
            heatmap.append((x, y, -1))

    return heatmap, edge_ids

locations = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        locations.append(tuple(map(int, line.split(', '))))

heatmap, edge_ids = process(locations)
# showgrid.show_heatmap(heatmap, s=10)
inner_ids = set(range(-1, len(locations)))
counter = Counter(list(map(lambda x: x[2], [h for h in heatmap if h[2] not in edge_ids])))
print(counter.most_common(1)[0][1])
print(datetime.datetime.now() - begin_time)
