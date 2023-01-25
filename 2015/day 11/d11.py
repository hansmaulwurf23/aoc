import datetime

begin_time = datetime.datetime.now()
forbidden = {'i', 'l', 'o'}


def is_valid(pwd):
    tripple = False
    pairs = 0
    lastpair = None
    last = None
    lad = None  # last ascii diff
    for i, c in enumerate(pwd):
        if c in forbidden:
            return False
        if last == c and c != lastpair:
            lastpair = c
            pairs += 1
            lad = 0
        elif last is not None:
            if lad == 1 and ord(last) + 1 == ord(c):
                tripple = True
            lad = ord(c) - ord(last)
        last = c

    return tripple and pairs > 1


def gen_next_pwd(pwd):
    new_chars = list(pwd)
    i = len(new_chars) - 1
    while i >= 0:
        c = new_chars[i]
        newc = ord(c) + 1
        while chr(newc) in {'i', 'l', 'o'}:
            newc += 1
        if newc > ord('z'):
            newc = ord('a') + (newc - ord('z') - 1)
            new_chars[i] = chr(newc)
            i -= 1
        else:
            new_chars[i] = chr(newc)
            break

    new_pwd = ''.join(new_chars)
    return new_pwd


def next_pwd(pwd):
    while True:
        pwd = gen_next_pwd(pwd)
        if is_valid(pwd):
            return pwd


# assert is_valid('hijklmmn') == False
# assert is_valid('abbceffg') == False
# assert is_valid('abbcegjk') == False
# assert next_pwd('abcdefgh') == 'abcdffaa'
# assert next_pwd('ghijklmn') == 'ghjaabcc'

npwd = next_pwd('hxbxwxba')
print(npwd)
print(next_pwd(npwd))

print(datetime.datetime.now() - begin_time)
