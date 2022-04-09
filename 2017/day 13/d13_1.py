import datetime

begin_time = datetime.datetime.now()
layers = []


def run(layers):
    severity = 0
    for depth, range in layers:
        time = depth
        scanner = time % (2 * (range - 1))
        if scanner == 0:
            severity += depth * range

    return severity


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        depth, range = list(map(int, line.split(': ')))
        layers.append([depth, range])

# print(run([(0, 3), (1, 2), (4, 4), (6, 4)]))
print(run(layers))
print(datetime.datetime.now() - begin_time)
