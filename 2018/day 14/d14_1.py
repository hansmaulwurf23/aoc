import datetime

begin_time = datetime.datetime.now()


def cycle(recip_scores, elf_idxes):
    new_scores = map(int, str(sum([recip_scores[i] for i in elf_idxes])))
    new_elf_idxes = []
    recip_scores.extend(new_scores)
    for elf_idx in elf_idxes:
        new_elf_idxes.append((elf_idx + 1 + recip_scores[elf_idx]) % len(recip_scores))

    return recip_scores, new_elf_idxes


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
elf_idxes = [0, 1]
after_recips = int(initial)
while True:
    recip_scores, elf_idxes = cycle(recip_scores, elf_idxes)
    # print_state(recip_scores, elf_idxes)
    if len(recip_scores) >= after_recips + 10:
        print(''.join(map(str, recip_scores[after_recips:after_recips+10])))
        break

print(datetime.datetime.now() - begin_time)