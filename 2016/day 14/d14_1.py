import datetime
from collections import defaultdict
from hashlib import md5

begin_time = datetime.datetime.now()
prefix, max_age = 'zpqevtbw', 1000
# prefix, max_age = 'abc', 1000


def find_good_stuff(hexhash):
    i = 0
    last = None
    tripple = None
    quintuple = None
    while i < len(hexhash) and (not tripple or not quintuple):
        if hexhash[i] != last:
            last = hexhash[i]
            i += 1
        elif i < len(hexhash) - 3 and hexhash[i + 1] == hexhash[i + 2] == hexhash[i + 3] == last:
            if quintuple is None: quintuple = last
            if tripple is None: tripple = last
            i += 4
        elif i < len(hexhash) - 1 and hexhash[i + 1] == last:
            if tripple is None: tripple = last
            i += 2
        else:
            i += 1

    return tripple, quintuple

def find_matching_keys():
    tripples = defaultdict(list)
    i = 0
    valid = 0
    while True:
        v = f'{prefix}{i}'
        h = md5(v.encode()).hexdigest()
        tripple, five = find_good_stuff(h)

        if five:
            if tripples[five][0] + max_age < i:
                tripples[five] = list(filter(lambda x: x + max_age >= i, tripples[five]))
            if len(tripples[five]) >= 2:
                for kidx in tripples[five]:
                    valid += 1
                    if valid == 64:
                        return kidx

                tripples[five] = []

        if tripple:
            tripples[tripple].append(i)

        i += 1


print(find_matching_keys())
print(datetime.datetime.now() - begin_time)
