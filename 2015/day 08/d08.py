import datetime

begin_time = datetime.datetime.now()
lines = [l.rstrip() for l in open('./input.txt').readlines()]
transition = str.maketrans({'"': '\\"', '\\': '\\\\'})
raw = sum([len(line) for line in lines])
net = sum([len(eval(line)) for line in lines])
esc = sum([len(f'"{line.translate(transition)}"') for line in lines])
print(f'part 1: {raw - net}')
print(f'part 1: {esc - raw}')
print(datetime.datetime.now() - begin_time)
