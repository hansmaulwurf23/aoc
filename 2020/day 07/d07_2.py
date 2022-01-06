canHold = {}
heldBy = {}

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        if line.endswith('contain no other bags.'):
            continue
        (srcColor, contents) = line.split(' bags contain ')
        if srcColor not in canHold.keys():
            canHold[srcColor] = {}
        for content in contents.split(', '):
            (cnt, dstColor) = content[0:(content.index(' bag'))].split(' ', maxsplit=1)
            canHold[srcColor][dstColor.strip()] = int(cnt)
            if dstColor not in heldBy.keys():
                heldBy[dstColor] = []
            heldBy[dstColor].append(srcColor)


def add_rec(cur_color):
    if cur_color not in canHold.keys():
        return 0

    intermediateSum = 0
    for nextColor, cnt in canHold[cur_color].items():
        intermediateSum += (cnt * add_rec(nextColor)) + cnt

    return intermediateSum


print(add_rec('shiny gold'))
print('7255 >')
