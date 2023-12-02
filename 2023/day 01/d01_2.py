import datetime

begin_time = datetime.datetime.now()
text_digits = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
               'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

with open('./input.txt') as f:
    sum = 0
    while line := f.readline().rstrip():
        digits = []
        for i, c in enumerate(line):
            if i + 3 <= len(line) and line[i:i+3] in text_digits:
                digits.append(text_digits[line[i:i+3]])
            elif i + 4 <= len(line) and line[i:i+4] in text_digits:
                digits.append(text_digits[line[i:i+4]])
            elif i + 5 <= len(line) and line[i:i+5] in text_digits:
                digits.append(text_digits[line[i:i+5]])
            elif '0' <= c <= '9':
                digits.append(int(c))
        # print(digits, digits[0], digits[-1], line)
        sum += (digits[0] * 10) + digits[-1]

print(sum)
print(datetime.datetime.now() - begin_time)
