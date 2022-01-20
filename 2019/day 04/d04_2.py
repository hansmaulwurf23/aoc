import datetime
from collections import deque

begin_time = datetime.datetime.now()

global_range = range(183564, 657474 + 1)
valid_counter = 0
for six in range(1, max(global_range) // pow(10, 5)):
    for five in [_ for _ in range(1, 10) if _ >= six]:
        for four in [_ for _ in range(1, 10) if _ >= five]:
            for three in [_ for _ in range(1, 10) if _ >= four]:
                for two in [_ for _ in range(1, 10) if _ >= three]:
                    for one in [_ for _ in range(1, 10) if _ >= two]:
                        digits = [six, five, four, three, two, one]
                        passwd = sum([pow(10, i) * x for i, x in enumerate(reversed(digits))])

                        # must be in range
                        if passwd not in global_range:
                            break

                        # two and only two digits must be the same
                        same_counter = 1
                        for i, j in zip(range(5), range(1, 6)):
                            if digits[i] == digits[j]:
                                same_counter += 1
                            else:
                                if same_counter == 2:
                                    break
                                else:
                                    same_counter = 1
                        if same_counter == 2:
                            valid_counter += 1

print(valid_counter)
print(datetime.datetime.now() - begin_time)
