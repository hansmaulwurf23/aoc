canHold = {}
heldBy = {}

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        if line.endswith('contain no other bags.'):
            continue
        (srcColor, contents) = line.split(' bags contain ')
        if srcColor not in canHold.keys():
            canHold[srcColor] = []
        for content in contents.split(', '):
            (cnt, dstColor) = content[0:(content.index(' bag'))].split(' ', maxsplit=1)
            canHold[srcColor].append([int(cnt), dstColor.strip()])
            if dstColor not in heldBy.keys():
                heldBy[dstColor] = []
            heldBy[dstColor].append(srcColor)

holdingColors = set()


def add_rec(cur_color):
    if cur_color not in heldBy.keys():
        return

    for nextColor in heldBy[cur_color]:
        holdingColors.add(nextColor)
        add_rec(nextColor)


add_rec('shiny gold')
print(len(holdingColors))
