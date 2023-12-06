import datetime
import math
import re
from collections import deque
from aopython import merge_ranges

begin_time = datetime.datetime.now()

mappings = [dict()]
with open('./input.txt') as f:
    lines = list(map(lambda x: x.rstrip(), f.readlines()))
    todo_ranges = list(map(int, re.findall(f'\d+', lines[0])))
    todo_ranges = deque(merge_ranges(list(map(lambda x, y: range(x, x + y), todo_ranges[::2], todo_ranges[1::2]))))

    i = 3
    while i < len(lines):
        if not lines[i].rstrip():
            i += 2
            mappings.append(dict())
        else:
            dest, source, size = map(int, lines[i].split())
            mappings[-1][range(source, source + size)] = dest - source
            i += 1

min_loc = math.inf
for mapping in mappings:
    new_ranges = []
    while todo_ranges:
        todo_range = todo_ranges.popleft()
        mapped = False
        for source_range, delta in mapping.items():
            if todo_range.start in source_range:
                new_ranges.append(range(todo_range.start + delta, min(source_range.stop, todo_range.stop) + delta))
                if todo_range.stop > source_range.stop:
                    todo_ranges.append(range(source_range.stop, todo_range.stop))
                mapped = True
                break
            elif source_range.start in todo_range:
                todo_ranges.append(range(todo_range.start, source_range.start))
                new_ranges.append(range(source_range.start + delta, min(source_range.stop, todo_range.stop) + delta))
                if todo_range.stop > source_range.stop:
                    todo_ranges.append(range(source_range.stop, todo_range.stop))
                mapped = True
                break
        if not mapped:
            new_ranges.append(todo_range)
    todo_ranges = deque(merge_ranges(new_ranges))

min_loc = min([m.start for m in todo_ranges])

print(min_loc)
print(datetime.datetime.now() - begin_time)
