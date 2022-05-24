import datetime
import re
from collections import Counter

begin_time = datetime.datetime.now()

offset = ord('a')

def decrypt(crypted, shifts):
    decrypted = []
    shifts = shifts % 26
    for c in crypted:
        if c == '-':
            decrypted.append(' ')
        else:
            decrypted.append(chr((ord(c) - offset + shifts) % 26 + offset))

    return ''.join(decrypted)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        name, id, chksm = re.match(r"([^0-9]+)(\d+)\[(.*)\]", line).groups()
        if ''.join(map(lambda x: x[0], Counter(sorted(name.replace('-', ''))).most_common(5))) == chksm:
            decr = decrypt(name, int(id))
            if re.match('northpole', decr):
                print(decrypt(name, int(id)), id)

print(datetime.datetime.now() - begin_time)
