import datetime

begin_time = datetime.datetime.now()


def cycle(recip_scores, e1, e2):
    nsum = recip_scores[e1] + recip_scores[e2]
    if nsum > 9:
        recip_scores.append(nsum // 10)
        recip_scores.append(nsum % 10)
    else:
        recip_scores.append(nsum)
    e1 = (e1 + 1 + recip_scores[e1]) % len(recip_scores)
    e2 = (e2 + 1 + recip_scores[e2]) % len(recip_scores)

    return recip_scores, e1, e2


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
max_runs = 1000000000
while True:
    max_runs -= 1
    if not max_runs:
        break
    recip_scores, e1, e2 = cycle(recip_scores, e1, e2)
    # print_state(recip_scores, elf_idxes)
    if len(recip_scores) >= len(pattern) and tuple(recip_scores[-len(pattern):]) == pattern:
        print(len(recip_scores) - len(pattern))
        break

print(datetime.datetime.now() - begin_time)