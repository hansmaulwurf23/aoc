import copy
import datetime
import re
begin_time = datetime.datetime.now()

UNITS, HP, DAMAGE, DAMAGE_TYPE, IMMUNE, WEAK, INITIATIVE, ARMY = range(8)
IMUSYS, INFECT = range(2)
opponent_army = {IMUSYS: INFECT, INFECT: IMUSYS}
army_names = ['Immune System', 'Infection']


def effective_power(group):
    return group[UNITS] * group[DAMAGE]


def calc_damage(attacking, defending):
    if attacking[DAMAGE_TYPE] in defending[WEAK]:
        factor = 2
    elif attacking[DAMAGE_TYPE] not in defending[IMMUNE]:
        factor = 1
    else:
        factor = 0
    return effective_power(attacking) * factor


def fight(armies):
    # target selection phase
    possible_ops = []
    for army_idx in range(len(armies)):
        possible_ops.append([g for g in armies[army_idx] if g[UNITS] > 0])

    fights = []
    for group in sorted(armies[0] + armies[1], key=lambda g: (effective_power(g), g[INITIATIVE]), reverse=True):
        my_army = group[ARMY]
        other_army = opponent_army[my_army]
        if len(possible_ops[other_army]) == 0:
            continue
        opponent = max(possible_ops[other_army], key=lambda o: (calc_damage(group, o), effective_power(o), o[INITIATIVE]))
        if calc_damage(group, opponent) > 0:
            fights.append(((my_army, armies[my_army].index(group)), (other_army, armies[other_army].index(opponent))))
            possible_ops[other_army].remove(opponent)

    # attacking phase
    dealt_damage = False
    for (my_army, my_idx), (other_army, other_idx) in sorted(fights, key=lambda pair: armies[pair[0][0]][pair[0][1]][INITIATIVE], reverse=True):
        group = armies[my_army][my_idx]
        opponent = armies[other_army][other_idx]
        # print(f'{group[UNITS]} -> {opponent[UNITS]}')

        damage = calc_damage(group, opponent)
        killed_units = min(opponent[UNITS], damage // opponent[HP])
        if killed_units > 0:
            dealt_damage = True
        opponent[UNITS] = opponent[UNITS] - killed_units

    return dealt_damage


def battle(boost):
    print(f'battle with boost {boost}')
    boost_armies = copy.deepcopy(org_armies)
    for g in boost_armies[IMUSYS]:
        g[DAMAGE] += boost
    while all(scores := [sum([g[UNITS] for g in army]) for army in boost_armies]):
        dealt_damage = fight(boost_armies)
        # print(scores)
        if not dealt_damage:
            return scores

    return scores


with open('./input.txt') as f:
    lines = f.readlines()
    org_armies = []
    cur_type = 0

    for line in lines:
        if line.find(':') > 0:
            org_armies.append([])
            continue
        if not line.rstrip():
            cur_type += 1
            continue

        s = re.match(r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)", line).groups()
        units, hp, specials, damage, damage_type, initiative = s
        immune = []
        weak = []
        if specials:
            for s in specials[1:-2].split("; "):
                if s.startswith("weak to "):
                    weak = s[len("weak to "):].split(", ")
                elif s.startswith("immune to "):
                    immune = s[len("immune to "):].split(", ")
        u = [int(units), int(hp), int(damage), damage_type, set(immune), set(weak), int(initiative), cur_type]
        org_armies[-1].append(u)


boost = 1
while True:
    scores = battle(boost)
    if scores[IMUSYS] > 0 and scores[INFECT] == 0:
        print(scores[IMUSYS])
        break
    else:
        boost += 1

print(datetime.datetime.now() - begin_time)
