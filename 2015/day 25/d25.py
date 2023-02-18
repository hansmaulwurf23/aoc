import datetime
import re

begin_time = datetime.datetime.now()

# (4,3) 19 = s(4) + 4 + 5 = s(4) + s(r+c-2=5) - s(3)
# (2,5) 17 = s(2) + 2 + 3 + 4 + 5 = s(2) + s(r+c-2=5) - s(1)
# (3,4) 18 = s(3) + 3 + 4 + 5 = s(3) + s(r+c-2=5) - s(2)
# (c,r) i = s(c) + s(c+r-2) - s(c-1)
#         = c(c+1)/2 + (c+r-2)(c+r-1)/2 + (c-1)c/2
#         = ((c+r-2)(c+r-1) - (c-1)c + c(c+1)) / 2 [1]
#
#    | 1   2   3   4   5   6   7   8   9
# ---+---+---+---+---+---+---+---+---+---+
#  1 |  1   3   6  10  15  21  28  36  45
#  2 |  2   5   9  14  20  27  35
#  3 |  4   8  13  19  26  34
#  4 |  7  12  18  25  33
#  5 | 11  17  24  32
#  6 | 16  23  31


r, c = map(int, re.findall(r'\d+', open('./input.txt').readline()))
mully, moddy, val = 252533, 33554393, 20151125
# see [1]
idx = (((r + c - 2) * (r + c - 1) - (c * (c - 1))) + (c * (c + 1))) // 2
for _ in range(idx - 1):
    val = (val * mully) % moddy

print(val)
print(datetime.datetime.now() - begin_time)
