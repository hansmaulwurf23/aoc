import datetime
from collections import deque

begin_time = datetime.datetime.now()
FWD = 303
# FWD = 3
ring_buf = deque()
for i in range(2018):
    ring_buf.rotate(-FWD)
    ring_buf.append(i)

print(ring_buf[0])
print(datetime.datetime.now() - begin_time)
