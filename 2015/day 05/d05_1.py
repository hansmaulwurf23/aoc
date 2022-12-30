import datetime
import re

begin_time = datetime.datetime.now()


def is_nice(phrase: str):
    return len(re.findall(r'a|e|i|o|u', phrase)) >= 3 and \
           any([True if phrase[i] == phrase[i+1] else False for i in range(len(phrase) - 1)]) and \
           not re.findall(r'ab|cd|pq|xy', phrase)


print(sum([1 if is_nice(l.rstrip()) else 0 for l in open('./input.txt').readlines()]))
print(datetime.datetime.now() - begin_time)
