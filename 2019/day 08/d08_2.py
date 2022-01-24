import datetime
from collections import Counter
begin_time = datetime.datetime.now()

height = 6
width = 25
image = list([['2'] * width for _ in range(height)])
val_map = {'2': ' ', '1': '#', '0': ' '}

with open('./input.txt') as f:
    data = f.readlines()[0].rstrip()

for l in range(len(data) // (width * height)):
    for y in range(height):
        for x in range(width):
            if image[y][x] == '2':
                image[y][x] = data[l * width * height + y * width + x]

for y in range(height):
    print(' '.join([val_map[_] for _ in image[y]]))

print(datetime.datetime.now() - begin_time)
