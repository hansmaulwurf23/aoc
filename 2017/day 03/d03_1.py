import datetime
import math

begin_time = datetime.datetime.now()

def calc_dist(v):
    r = math.ceil(math.sqrt(v))
    ring = r // 2

    max_in_ring = (ring * 2 + 1) ** 2
    zero_offsets = [max_in_ring - x * ring for x in [1, 3, 5, 7]]

    return ring + min([abs(v - x) for x in zero_offsets])


print(calc_dist(312051))

print(datetime.datetime.now() - begin_time)
