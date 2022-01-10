import datetime

begin_time = datetime.datetime.now()
opPrecedence = {'+': 3, '*': 2}

# computes arithmetic in reversed polish notation (coming from the shunting algorithm)
def computeRPN(input):
    calcStack = []
    for i in input:
        if i == '+':
            calcStack.append(calcStack.pop() + calcStack.pop())
        elif i == '*':
            calcStack.append(calcStack.pop() * calcStack.pop())
        else:
            calcStack.append(i)

    return calcStack.pop()


# implements a shunting yard algorithm with 'wrong' operator precedence
def shunting_yard(elems):
    pos = 0
    output = []
    opStack = []

    while pos < len(elems):
        e = elems[pos]
        if e == '(':
            opStack.append(e)
        elif e in ('*', '+'):
            while len(opStack) and opStack[-1] != '(' and opPrecedence[opStack[-1]] > opPrecedence[e]:
                output.append(opStack.pop())
            opStack.append(e)
        elif e == ')':
            while len(opStack) and opStack[-1] != '(':
                output.append(opStack.pop())
            opStack.pop()
        else:
            output.append(int(e))

        pos += 1

    while len(opStack):
        output.append(opStack.pop())

    return output


inputSum = 0
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        res = computeRPN(shunting_yard(list(line.replace(' ', ''))))
        inputSum += res

print(inputSum)
print(datetime.datetime.now() - begin_time)
