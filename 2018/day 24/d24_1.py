import copy
import datetime
import re
begin_time = datetime.datetime.now()

UNITS, HP, DAMAGE, DAMAGE_TYPE, IMMUNE, WEAK, INITIATIVE, ARMY = range(8)
IMUSYS, INFECT = range(2)
opponent_army = {IMUSYS: INFECT, INFECT: IMUSYS}
army_names = ['Immune System', 'Infection']
DEBUG = True


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


def dump_armies(armies):
    print(f'{"="*80}')
    for army_idx, name in enumerate(army_names):
        print(f'{name}:')
        print('\n'.join(map(lambda g: f'Group {g[0]+1} contains {g[1][UNITS]} units', enumerate(armies[army_idx]))))
    print('\n')


def dump_fight(fight, armies):
    (my_army, my_idx), (other_army, other_idx) = fight
    group = armies[my_army][my_idx]
    opp = armies[other_army][other_idx]
    print(f'{army_names[my_army]} group {my_idx+1} would deal {army_names[other_army]} {other_idx+1} {calc_damage(group, opp)}')


def dump_attack(fight, killed):
    (my_army, my_idx), (other_army, other_idx) = fight
    print(f'{army_names[my_army]} group {my_idx+1} attacks {army_names[other_army]} {other_idx+1}, killing {killed} units')


def fight(armies):
    # target selection phase
    possible_ops = []
    for army_idx in range(len(armies)):
        possible_ops.append([])
        for group in armies[army_idx]:
            if group[UNITS]:
                possible_ops[-1].append(group.copy())

    if DEBUG: dump_armies(possible_ops)
    fights = []
    for group in sorted(armies[0] + armies[1], key=lambda g: (effective_power(g), g[INITIATIVE]), reverse=True):
        # print((effective_power(group), group[INITIATIVE]))
        my_army = group[ARMY]
        other_army = opponent_army[my_army]
        if len(possible_ops[other_army]) == 0:
            continue
        opponent = max(possible_ops[other_army], key=lambda o: (calc_damage(group, o), effective_power(o), o[INITIATIVE]))
        if calc_damage(group, opponent):
            fights.append(((my_army, armies[my_army].index(group)), (other_army, armies[other_army].index(opponent))))
            if DEBUG: dump_fight(fights[-1], armies)
            possible_ops[other_army].remove(opponent)

    if DEBUG: print('\n')

    # attacking phase
    for (my_army, my_idx), (other_army, other_idx) in sorted(fights, key=lambda pair: armies[pair[0][0]][pair[0][1]][INITIATIVE], reverse=True):
        group = armies[my_army][my_idx]
        opponent = armies[other_army][other_idx]
        if group[UNITS] == 0:
            continue

        killed_units = calc_damage(group, opponent) // opponent[HP]
        if DEBUG: dump_attack(((my_army, my_idx), (other_army, other_idx)), killed_units)
        opponent[UNITS] = max([0, opponent[UNITS] - killed_units])


with open('./input.txt') as f:
    lines = f.readlines()
    armies = []
    cur_type = 0

    for line in lines:
        if line.find(':') > 0:
            armies.append([])
            continue
        if not line.rstrip():
            cur_type += 1
            continue

        s = re.match(r"(\d+) units each with (\d+) hit points (\([^)]*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)", line).groups()
        units, hp, specials, damage, damage_type, initiative = s
        immune = []
        weak = []
        if specials:
            specials = specials.rstrip(" )").lstrip("(")
            for s in specials.split("; "):
                if s.startswith("weak to "):
                    weak = s[len("weak to "):].split(", ")
                elif s.startswith("immune to "):
                    immune = s[len("immune to "):].split(", ")
        u = [int(units), int(hp), int(damage), damage_type, set(immune), set(weak), int(initiative), cur_type]
        armies[-1].append(u)

while all([sum([g[UNITS] for g in army]) for army in armies]):
    fight(armies)

dump_armies(armies)
print(max([sum([g[UNITS] for g in army]) for army in armies]))
print('19555 too low')
print(datetime.datetime.now() - begin_time)
