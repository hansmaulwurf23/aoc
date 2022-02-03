import datetime
begin_time = datetime.datetime.now()

ASCII_CASE_DIFF = ord('a') - ord('A')


def react_and_filter(input, filters):
    output = []
    for c in input:
        if c in filters:
            continue

        if len(output) and abs(ord(output[-1]) - ord(c)) == ASCII_CASE_DIFF:
            output.pop()
            continue
        else:
            output.append(c)

    return output

with open('./input.txt') as f:
    line = list(f.readlines()[0].rstrip())

print(min([len(react_and_filter(line, {chr(i), chr(i + ASCII_CASE_DIFF)})) for i in range(ord('A'), ord('Z') + 1)]))
print(datetime.datetime.now() - begin_time)
