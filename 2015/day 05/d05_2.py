import datetime
import re
from collections import defaultdict, Counter

begin_time = datetime.datetime.now()


def is_nice(phrase: str):
    rule_one = False
    pairs = defaultdict(int)
    for i, (a, b) in enumerate(zip(phrase, phrase[1:])):
        key = f'{a}{b}'
        if key in pairs:
            if pairs[key] + 1 < i:
                rule_one = True
                break
        else:
            pairs[key] = i

    rule_two = any([a == c for a, b, c in zip(phrase, phrase[1:], phrase[2:])])
    rule_tgx = re.search(r'(.).\1', phrase) is not None

    if rule_tgx != rule_two:
        print(f'{phrase} rule two {rule_two} <-> rule tgx {rule_tgx}')

    return rule_one and rule_two


print(sum([1 if is_nice(l.rstrip()) else 0 for l in open('./input.txt').readlines()]))
print(datetime.datetime.now() - begin_time)
