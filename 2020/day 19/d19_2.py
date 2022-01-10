import datetime
import re

begin_time = datetime.datetime.now()

rules = dict()
leafs = dict()


def flatten(t):
    return [item for sublist in t for item in sublist]


def explode(ruleNo):
    if ruleNo in leafs.keys():
        return leafs[ruleNo]
    else:
        rule = rules[ruleNo]

    result = '(' + '|'.join([''.join([explode(r) for r in orRules if r != ruleNo]) for orRules in rule]) + ')'

    if ruleNo in flatten(rule):
        result += '+'

    leafs[ruleNo] = result
    return result

with open('./input.txt') as file:
    # rules
    while line := file.readline().rstrip():
        # was '42 | 42 8' which is the same thing, this one is handled in the regex
        if line.startswith('8: '): line = "8: 42 8"
        # was '11: 42 31 | 42 11 31'. now we match one and two mirrored 42's and 31's and do the rest here [A]
        if line.startswith('11: '): line = "11: 42 31 | 42 42 31 31"

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
    special = leafs['42'] + leafs['31']
    while line := file.readline().rstrip():
        if regex.match(line):
            matchingMessages += 1
        else:
            while len(line) and re.match(special, line):
                # [A] we recursively replace matches of 42 31 with nothing and see if the line still exists and
                # finally matches the big fat regex
                line = re.sub(special, '', line)
                if regex.match(line):
                    matchingMessages += 1


print(matchingMessages)
print(datetime.datetime.now() - begin_time)
