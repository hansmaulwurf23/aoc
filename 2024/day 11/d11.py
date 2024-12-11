import datetime
from collections import Counter, defaultdict

begin_time = datetime.datetime.now()

def blink(numbers: dict, rest):
    if rest == 0:
        return numbers

    new_numbers = defaultdict(int)
    for number, count in numbers.items():
        strnum = str(number)
        if number == 0:
            new_numbers[1] += count
        elif (digits := len(strnum)) % 2 == 0:
            new_numbers[int(strnum[:digits // 2])] += count
            new_numbers[int(strnum[digits // 2:])] += count
        else:
            new_numbers[number * 2024] += count

    return blink(new_numbers, rest - 1)


with open('./input.txt') as f:
    numbers = Counter(list(map(int, f.readline().rstrip().split())))

numbers = blink(numbers, 25)
print(f'part 1: {sum(numbers.values())}')
numbers = blink(numbers, 50)
print(f'part 2: {sum(numbers.values())}')
print(datetime.datetime.now() - begin_time)
