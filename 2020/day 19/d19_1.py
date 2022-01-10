import datetime
import re

begin_time = datetime.datetime.now()

rules = dict()
leafs = dict()

def explode(ruleNo):
    if ruleNo in leafs.keys():
        return leafs[ruleNo]
    else:
        rule = rules[ruleNo]

    result = '(' + '|'.join([''.join([explode(r) for r in orRules]) for orRules in rule]) + ')'

    leafs[ruleNo] = result
    return result

with open('./input.txt') as file:
    # rules
    while line := file.readline().rstrip():
        (ruleNo, ruleDefs) = line.split(': ')
        for ruleDef in ruleDefs.split(' | '):
            if ruleDef.startswith('"'):
                leafs[ruleNo] = ruleDef.replace('"', '')
            else:
                if ruleNo not in rules.keys():
                    rules[ruleNo] = []   # ORs
                rules[ruleNo].append(ruleDef.split(' '))

    regex = re.compile('^' + explode('0') + '$')

    # messages
    matchingMessages = 0
    while line := file.readline().rstrip():
        if regex.match(line):
            matchingMessages += 1


print(matchingMessages)
print(datetime.datetime.now() - begin_time)
