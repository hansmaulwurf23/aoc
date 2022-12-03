import datetime

begin_time = datetime.datetime.now()

val_sum = 0

with open('./input.txt') as f:
    group_counter = 0
    while line := f.readline().rstrip():
        items = set(line)
        group_counter += 1

        if group_counter == 1:
            same_items = set(items)
        else:
            same_items = items.intersection(same_items)

        if group_counter == 3:
            same = list(same_items)[0]
            v = ord(same[0]) - ord('A')
            if ord(same) >= ord('a'):
                v = ord(same) - ord('a') + 1
            else:
                v = ord(same) - ord('A') + 27

            val_sum += v
            group_counter = 0

print(val_sum)
print(datetime.datetime.now() - begin_time)
