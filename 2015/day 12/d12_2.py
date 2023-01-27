import datetime
import json

begin_time = datetime.datetime.now()


def sum_rec(doc):
    if isinstance(doc, list):
        for e in doc:
            return sum([e if isinstance(e, int) else sum_rec(e) for e in doc])
    elif isinstance(doc, dict):
        for k, v in doc.items():
            if v == 'red':
                return 0
        return sum([sum_rec(v) for v in doc.values()])
    else:
        return doc if isinstance(doc, int) else 0


print(sum_rec(json.load(open('./input.txt'))))
print(datetime.datetime.now() - begin_time)
