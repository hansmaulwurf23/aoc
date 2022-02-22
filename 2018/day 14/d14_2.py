import datetime

begin_time = datetime.datetime.now()


def cycle(recip_scores, e1, e2):
    nsum = recip_scores[e1] + recip_scores[e2]
    added = 1
    if nsum > 9:
        recip_scores.append(nsum // 10)
        recip_scores.append(nsum % 10)
        added = 2
    else:
        recip_scores.append(nsum)

    lenny = len(recip_scores)
    e1 = (e1 + 1 + recip_scores[e1]) % lenny
    e2 = (e2 + 1 + recip_scores[e2]) % lenny

    return recip_scores, e1, e2, added


def print_state(recip_scores, elf_idxes):
    for i, score in enumerate(recip_scores):
        if i not in elf_idxes:
            print(f' {score} ', end='')
        else:
            if elf_idxes.index(i) == 1:
                print(f'[{score}]', end='')
            else:
                print(f'({score})', end='')

    print('')

initial = '236021'

recip_scores = [3, 7]
e1, e2 = [0, 1]
# pattern = tuple(map(int, '59414'))
pattern = tuple(map(int, initial))
patlen = len(pattern)
while True:
    recip_scores, e1, e2, added = cycle(recip_scores, e1, e2)
    # print_state(recip_scores, elf_idxes)
    if len(recip_scores) < patlen:
        continue
    if tuple(recip_scores[-patlen:]) == pattern or (added == 2 and tuple(recip_scores[-patlen - 1:-1]) == pattern):
        print(len(recip_scores) - patlen - (added - 1))
        break

# probably because sometimes two digits are appended!
print(datetime.datetime.now() - begin_time)