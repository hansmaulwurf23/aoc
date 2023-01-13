import datetime
from collections import deque
begin_time = datetime.datetime.now()


def party(elves_count):
    takers = deque(range(1, elves_count // 2 + 1))
    givers = deque(range(elves_count // 2 + 1, elves_count + 1))
    party_ppl = elves_count
    while party_ppl > 1:
        givers.append(takers.popleft())
        givers.popleft()
        if party_ppl % 2:
            takers.append(givers.popleft())
        party_ppl -= 1

    return givers.popleft()

print(party(3004953))
print(datetime.datetime.now() - begin_time)
