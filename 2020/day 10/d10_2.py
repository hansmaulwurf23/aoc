import datetime

begin_time = datetime.datetime.now()
adapters = [0]

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        adapters.append(int(line))

adapters = sorted(adapters)
reachByPaths = {x: 0 for x in adapters}
for i, n in enumerate(adapters):
    if n == 0:
        reachByPaths[0] = 1
        continue

    lookBackIndex = i - 3
    if (lookBackIndex < 0): lookBackIndex = 0

    for j in range(lookBackIndex, i):
        if n - adapters[j] <= 3:
            reachByPaths[n] += reachByPaths[adapters[j]]

print(reachByPaths[max(adapters)])
print(datetime.datetime.now() - begin_time)
