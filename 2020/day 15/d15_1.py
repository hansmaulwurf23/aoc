import datetime
begin_time = datetime.datetime.now()

input = [1, 2, 16, 19, 18, 0]
# input = [3, 1, 2]

visited = {int(x): i + 1 for i, x in enumerate(input)}
step = len(visited)
last = input[-1]
visited[last] = None
endSteps = 2020

while step < endSteps:
    if visited[last] == None:
        next = 0
        visited[last] = step
    else:
        next = step - visited[last]
        visited[last] = step

    if next not in visited.keys():
        visited[next] = None

    step += 1
    last = next

print(last)
print(datetime.datetime.now() - begin_time)
