import datetime
import itertools

begin_time = datetime.datetime.now()

HP, DMG, ARM = range(3)
COST = 0
ME, BOSS = range(2)

shop_items = {
    'weapons': [
        {'name': 'Dagger', 'vals': [8, 4, 0]},
        {'name': 'Shortsword', 'vals': [10, 5, 0]},
        {'name': 'Warhammer', 'vals': [25, 6, 0]},
        {'name': 'Longsword', 'vals': [40, 7, 0]},
        {'name': 'Greataxe', 'vals': [74, 8, 0]},
    ],
    'armor': [
        {'name': 'No Armore', 'vals': [0, 0, 0]},
        {'name': 'Leather', 'vals': [13, 0, 1]},
        {'name': 'Chainmail', 'vals': [31, 0, 2]},
        {'name': 'Splintmail', 'vals': [53, 0, 3]},
        {'name': 'Bandedmail', 'vals': [75, 0, 4]},
        {'name': 'Platemail', 'vals': [102, 0, 5]},
    ],
    'rings': [
        {'name': 'Damage +1', 'vals': [25, 1, 0]},
        {'name': 'Damage +2', 'vals': [50, 2, 0]},
        {'name': 'Damage +3', 'vals': [100, 3, 0]},
        {'name': 'Defense +1', 'vals': [20, 0, 1]},
        {'name': 'Defense +2', 'vals': [40, 0, 2]},
        {'name': 'Defense +3', 'vals': [80, 0, 3]},
    ]
}

with open('./input.txt') as f:
    boss = [int(l.split(': ')[1].rstrip()) for l in f.readlines()]


def fight(players):
    player, oppo = 0, 1
    while True:
        players[oppo][HP] -= max(1, players[player][DMG] - players[oppo][ARM])
        # print(f'player {oppo} goes down to {players[oppo][HP]} hit points')
        if players[oppo][HP] <= 0:
            return player

        player = (player + 1) % 2
        oppo = 1 - player


assert fight([[8, 5, 5], [12, 7, 2]]) == 0


def incubate_player(weapon, armor, rings):
    player = [100, 0, 0]
    cost = weapon['vals'][COST] + armor['vals'][COST]
    player[DMG] = weapon['vals'][DMG] + armor['vals'][DMG]
    player[ARM] = weapon['vals'][ARM] + armor['vals'][ARM]
    for r in (rings if rings else []):
        player[DMG] += r['vals'][DMG]
        player[ARM] += r['vals'][ARM]
        cost += r['vals'][COST]
    return player, cost


min_cost = 42424242
max_cost = 0
for weapon, armor in itertools.product(shop_items['weapons'], shop_items['armor']):
    for r in range(3):
        for rings in itertools.combinations(shop_items['rings'], r):
            player, cost = incubate_player(weapon, armor, rings)
            winner = fight([player, list(boss)])
            if winner == ME and cost < min_cost:
                min_cost = cost
            if winner == BOSS and cost > max_cost:
                max_cost = cost

print(f'part 1: {min_cost}')
print(f'part 2: {max_cost}')
print(datetime.datetime.now() - begin_time)
