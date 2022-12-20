import datetime
import re
import itertools
from collections import defaultdict
import functools

begin_time = datetime.datetime.now()
ORE, CLAY, OBSIDIAN, GEODE = range(4)
ID, COST = range(2)
RESNAMES = ['ORE', 'CLAY', 'OBSIDIAN', 'GEODE']
RUNTIME = 32
MAX_GEO = [(minute - 1) * minute // 2 for minute in range(RUNTIME + 1)]
cur_best = 0
cache = dict()
cache_hit = 0
cache_miss = 0

def calc_build_possibilities(bp, resources, robots, time_left, max_cost):
    possibles = []
    cst = bp[COST]

    if cst[GEODE][OBSIDIAN] <= resources[OBSIDIAN] and cst[GEODE][ORE] <= resources[ORE]:
        return [GEODE]

    if cst[OBSIDIAN][CLAY] <= resources[CLAY] and cst[OBSIDIAN][ORE] <= resources[ORE] and \
            robots[OBSIDIAN] * time_left + resources[OBSIDIAN] < time_left * max_cost[OBSIDIAN]:
        possibles.append(OBSIDIAN)

    if cst[CLAY][ORE] <= resources[ORE] and robots[CLAY] < max_cost[CLAY] and \
            robots[CLAY] * time_left + resources[CLAY] < time_left * max_cost[CLAY]:
        possibles.append(CLAY)

    if cst[ORE][ORE] <= resources[ORE] and \
            robots[ORE] * time_left + resources[ORE] < time_left * max_cost[ORE]:
        possibles.append(ORE)

    #if not possibles or (possibles[0] != OBSIDIAN and len(possibles) <= 2):
    possibles.append(None)

    return possibles


def run_plan(bp, robots, build_robot, resources, time_left, max_cost):
    global cur_best, cache, cache_hit, cache_miss

    if (tuple(robots), tuple(resources), time_left) in cache:
        cache_hit += 1
        return cache[(tuple(robots), tuple(resources), time_left)]
    else:
        cache_miss += 1

    # print(f'\n== Minute {RUNTIME - time_left + 1} {build_plan[0]} {resources} ==')
    if build_robot is not None:
        for res_type, res_count in bp[COST][build_robot].items():
            resources[res_type] -= res_count

    resources = [r + n for r, n in zip(resources, robots)]
    if build_robot is not None:
        robots[build_robot] += 1

    time_left -= 1
    if cur_best is not None and resources[GEODE] + robots[GEODE] * time_left + MAX_GEO[time_left] <= cur_best:
       return 0

    if time_left:
        v = simulate_blueprint(bp, robots, resources, time_left, max_cost)
        cache[(tuple(robots), tuple(resources), time_left)] = v
        return v
    else:
        if resources[GEODE] and (cur_best is None or resources[GEODE] > cur_best):
            cur_best = resources[GEODE]
        cache[(tuple(robots), tuple(resources), time_left)] = resources[GEODE]
        return resources[GEODE]


def simulate_blueprint(bp, robots, resources, time_left, max_cost):
    possibilities = calc_build_possibilities(bp, resources, robots, time_left, max_cost)
    #if time_left == 20:
    #    print(f'cache hits {cache_hit} miss {cache_miss} ({round(cache_hit / cache_miss * 100, 2)})')
    return max(map(lambda p: run_plan(bp, robots.copy(), p, resources.copy(), time_left, max_cost), possibilities))


def calc_blueprint_quality(bp):
    global cur_best, cache, cache_hit
    cache = dict()
    robots = [1, 0, 0, 0]
    resources = [0, 0, 0, 0]
    cur_best = None
    cache_hit = 0
    max_cost = [max(map(lambda c: c[r] if r in c else 0, bp[COST].values())) for r in range(len(RESNAMES))]
    return simulate_blueprint(bp, robots, resources, RUNTIME, max_cost)


blueprints = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        vals = tuple(map(int, re.findall(r'\d+', line)))
        blueprints.append((vals[0], {
            ORE: {ORE: vals[1]},
            CLAY: {ORE: vals[2]},
            OBSIDIAN: {ORE: vals[3], CLAY: vals[4]},
            GEODE: {ORE: vals[5], OBSIDIAN: vals[6]}
        }))


qualis = []
for i, bp in enumerate(blueprints[:3]):
    print(f'running bp {i + 1} for {RUNTIME} minutes @ {datetime.datetime.now()} ')
    qualis.append(calc_blueprint_quality(bp))
    print(f'max {qualis[-1]}')

print(qualis)
print(qualis[0] * qualis[1] * qualis[2])
print(datetime.datetime.now() - begin_time)
