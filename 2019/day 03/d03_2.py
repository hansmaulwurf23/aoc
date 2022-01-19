import datetime
from PIL import Image, ImageDraw, ImageOps
from aopython import min_max_2d, manhattan_distance

begin_time = datetime.datetime.now()

moving = {
    'U': [0, 1],
    'D': [0, -1],
    'R': [1, 0],
    'L': [-1, 0]
}


def fetch_all_coords_for_path(line):
    x, y = [0, 0]
    coords = dict()
    all_steps = 1
    for m in line.split(','):
        dir, steps = m[0], int(m[1:])
        xf, yf = moving[dir]
        for i in range(1, steps + 1):
            if (t := (x + (xf * i), y + (yf * i))) not in coords.keys():
                coords[t] = all_steps
            all_steps += 1

        x, y = [x + (xf * steps), y + (yf * steps)]

    return coords


def draw_image(paths, colors):
    fx, tx, fy, ty = min_max_2d(list(paths[0])+list(paths[1]))
    line_width = 5
    cross_size = 50

    with Image.new("RGB", (tx-fx, ty-fy)) as im:
        draw = ImageDraw.Draw(im)

        # draw center of coords
        draw.line([(-cross_size-fx, -cross_size-fy), (cross_size-fx, cross_size-fy)], width=line_width, fill='yellow')
        draw.line([(cross_size-fx, -cross_size-fy), (-cross_size-fx, cross_size-fy)], width=line_width, fill='yellow')

        for i, coords in enumerate(paths):
            prev = (0-fx, 0-fy)
            # for c in [(x-fx, y-fy) for (x, y) in coords]:
            draw.line([prev] + [(x-fx, y-fy) for (x, y) in coords], width=line_width, fill=colors[i])
            # prev = c
        scaled = ImageOps.scale(im, 0.2)
        scaled.save('/tmp/d03.png', "PNG")


def find_cross_points(line, coords):
    x, y = [0, 0]
    cross_points = dict()
    all_steps = 1
    for m in line.split(','):
        dir, steps = m[0], int(m[1:])
        xf, yf = moving[dir]
        for i in range(1, steps + 1):
            if (x + (xf * i), y + (yf * i)) in coords:
                cross_points[(x + (xf * i), y + (yf * i))] = [coords[(x + (xf * i), y + (yf * i))], all_steps]
            all_steps += 1
        x, y = [x + (xf * steps), y + (yf * steps)]

    return cross_points


with open('./input.txt') as f:
    lines = f.readlines()
    master = fetch_all_coords_for_path(lines[0])
    # draw_image([master.keys(), fetch_all_coords_for_path(lines[1]).keys()], ['red', 'green'])
    cross_points = find_cross_points(lines[1], master)


print(cross_points)
print(min(map(sum, cross_points.values())))
print(datetime.datetime.now() - begin_time)
