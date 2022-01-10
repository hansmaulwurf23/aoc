import datetime

begin_time = datetime.datetime.now()


def evalRec(elems, pos):
    result = 0
    operator = None
    operand = None

    while pos < len(elems):
        e = elems[pos]

        if e == '(':
            operand, pos = evalRec(elems, pos + 1)
        elif e == ')':
            return result, pos
        elif e in ['+', '*']:
            operator = e
            operand = None
        else:
            operand = int(e)

        if operator is None:
            result = operand
        elif operand is not None:
            if operator == '+':
                result += operand
            elif operator == '*':
                result *= operand

        pos += 1

    return result, pos


inputSum = 0
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        res, *_ = evalRec(list(line.replace(' ', '')), 0)
        inputSum += res

print(inputSum)
print(datetime.datetime.now() - begin_time)
