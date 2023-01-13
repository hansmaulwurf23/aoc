import datetime
from collections import deque
begin_time = datetime.datetime.now()


# seems to be this one: https://oeis.org/A172097
def present_party(elves_count):
    elves = deque(range(elves_count))
    party_ppl = len(elves)

    while party_ppl > 1:
        elves.rotate(-1)
        elves.popleft()
        party_ppl -= 1

    return elves.pop() + 1


# for i in range(1, 31, 2):
#     print(i, present_party(i))

print(present_party(3004953))
print(datetime.datetime.now() - begin_time)
