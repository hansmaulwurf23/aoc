import datetime
begin_time = datetime.datetime.now()


def count_in_line(line):
    return line.count('XMAS') + line.count('SAMX')

text, counter = [l.rstrip() for l in open('./input.txt').readlines()], 0
# horizontal
for line in text:
    counter += count_in_line(line)

# vertical
for x in range(len(text[0])):
    counter += count_in_line(''.join(l[x] for l in text))

# \ upper right
for t in range(len(text[0]) - 3):
    counter += count_in_line(''.join(text[y][x] for y, x in zip(range(len(text)), range(t, len(text[0])))))

# \ lower left
for t in range(1, len(text) - 3):
    counter += count_in_line(''.join(text[y][x] for y, x in zip(range(t, len(text)), range(len(text[0])))))

# / upper left
for t in range(len(text[0]) - 3):
    counter += count_in_line(''.join(text[y][x] for y, x in zip(range(len(text) - 1 - t, -1, -1), range(len(text[0])))))

# / lower right
for t in range(1, len(text) - 3):
    counter += count_in_line(''.join(text[y][x] for y, x in zip(range(len(text) - 1, -1, -1), range(t, len(text[0])))))

print(f'part 1: {counter}')

def in_block(b):
    return b[1][1] == 'A' and b[0][0] in 'MS' and (
        (b[0][0] == b[0][2] and b[2][0] == b[2][2] and b[2][0] in 'MS' and b[0][0] != b[2][0])
     or (b[0][0] == b[2][0] and b[0][2] == b[2][2] and b[0][2] in 'MS' and b[0][0] != b[0][2]))

counter = sum([in_block([line[x:x + 3] for line in text[y:y + 3]]) for y in range(len(text) - 2) for x in range(len(text[0]) - 2)])
print(f'part 2: {counter}')
print(datetime.datetime.now() - begin_time)
