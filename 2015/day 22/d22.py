import datetime
import functools

begin_time = datetime.datetime.now()

SHLD, SHLD_TURNS = 7, 6
POISN, POISN_TURNS = 3, 6
RECH, RECH_TURNS = 101, 5
ME, BOSS = range(2)

with open('./input.txt') as f:
    boss = [int(l.split(': ')[1].rstrip()) for l in f.readlines()]


@functools.cache
def round(player, cost, hp, mana, bhp, bdmg, effects, d):
    shield_left, poison_left, recharge_left = effects

    # difficulty adjustor
    hp -= d

    # player lost
    if hp <= 0:
        return None

    armor = 0
    if shield_left:
        armor = SHLD
        shield_left -= 1

    if poison_left:
        bhp -= POISN
        if bhp <= 0:
            return cost
        poison_left -= 1

    if recharge_left:
        mana += RECH
        recharge_left -= 1

    effects = (shield_left, poison_left, recharge_left)
    nxt_pl = 1 - player

    if player == BOSS:
        return round(nxt_pl, cost, hp - max(1, bdmg - armor), mana, bhp, bdmg, effects, d)

    # If you cannot afford to cast any spell, you lose
    if mana < 53:
        return None

    results = []
    if mana >= 53:
        results.append(round(nxt_pl, cost+53, hp, mana - 53, bhp - 4, bdmg, effects, d))

    if mana >= 73:
        results.append(round(nxt_pl, cost+73, hp + 2, mana - 73, bhp - 2, bdmg, effects, d))

    if not shield_left and mana >= 113:
        results.append(round(nxt_pl, cost+113, hp, mana - 113, bhp, bdmg, (SHLD_TURNS, poison_left, recharge_left), d))

    if not poison_left and mana >= 173:
        results.append(round(nxt_pl, cost+173, hp, mana - 173, bhp, bdmg, (shield_left, POISN_TURNS, recharge_left), d))

    if not recharge_left and mana >= 229:
        results.append(round(nxt_pl, cost+229, hp, mana - 229, bhp, bdmg, (shield_left, poison_left, RECH_TURNS), d))

    if any(results):
        return min(filter(lambda x: x is not None, results))
    else:
        return None


print(f'part 1: {round(0, 0, 50, 500, *boss, (0, 0, 0), 0)}')
print(f'part 2: {round(0, 0, 50, 500, *boss, (0, 0, 0), 1)}')
print(datetime.datetime.now() - begin_time)
