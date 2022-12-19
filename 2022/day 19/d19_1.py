import datetime
import re
import itertools
from collections import defaultdict
import functools

begin_time = datetime.datetime.now()
ORE, CLAY, OBSIDIAN, GEODE = range(4)
ID, COST = range(2)
RESNAMES = ['ORE', 'CLAY', 'OBSIDIAN', 'GEODE']
RUNTIME = 24
best_by_minute = dict()
cur_best = 0


def calc_build_possibilities(bp, resources, robots, max_cost):
    poss = dict()
    cst = bp[COST]

    geo = [1] if cst[GEODE][OBSIDIAN] <= resources[OBSIDIAN] and cst[GEODE][ORE] <= resources[ORE] else [0]
    obs = [1] if cst[OBSIDIAN][CLAY] <= resources[CLAY] and cst[OBSIDIAN][ORE] <= resources[ORE] else [0]
    cla = [0, 1] if cst[CLAY][ORE] <= resources[ORE] and robots[CLAY] < max_cost[CLAY] else [0]
    ore = [0, 1] if cst[ORE][ORE] <= resources[ORE] and robots[ORE] < max_cost[ORE] else [0]

    for combination in itertools.product(ore, cla, obs, geo):
        costs = defaultdict(int)
        for rob_type, rob_count in [(rt, rc) for rt, rc in enumerate(combination) if rc]:
            for res_type, res_count in bp[COST][rob_type].items():
                costs[res_type] += res_count
        if all(map(lambda r: costs[r] <= resources[r], costs)):
            poss[combination] = costs

    # try to minimize new states
    filtered = None
    if geo == [1]:
        # if we can build geo robot, do it!
        filtered = {k: v for k, v in poss.items() if k[GEODE]}
    elif obs == [1]:
        # if not, at least build the requirements to build a geo robot
        filtered = {k: v for k, v in poss.items() if k[OBSIDIAN]}
    elif len(poss) >= 3:
        # if we can build robots in different ways, do not build nothing
        filtered = {k: v for k, v in poss.items() if k != (0, 0, 0, 0)}

    if filtered:
        #max_new = max(map(lambda x: sum(x), filtered.keys()))
        #filtered = {k: v for k, v in filtered.items() if sum(k) == max_new}
        poss = filtered

    return sorted([(x, y) for x, y in poss.items()], reverse=True)


def run_plan(bp, robots, build_plan, resources, time_left, max_cost):
    global cur_best
    #print(f'\n== Minute {RUNTIME - time_left + 1} {build_plan[0]} {resources} ==')
    if build_plan:
        new_robots, costs = build_plan
        for rob_type, rob_count in [(rt, rc) for rt, rc in enumerate(new_robots) if rc]:
            for res_type, res_count in bp[COST][rob_type].items():
                resources[res_type] -= res_count

    resources = [r + n for r, n in zip(resources, robots)]
    robots = [r + n for r, n in zip(robots, new_robots)]

    time_left -= 1
    if resources[GEODE] + robots[GEODE] + (time_left * (time_left + 1) // 2) <= cur_best:
        return 0

    if time_left:
        return simulate_blueprint(bp, robots, resources, time_left, max_cost)
    else:
        if resources[GEODE] > cur_best:
            cur_best = resources[GEODE]
        return resources[GEODE]


def simulate_blueprint(bp, robots, resources, time_left, max_cost):
    possibilities = calc_build_possibilities(bp, tuple(resources), robots, max_cost)
    if not possibilities:
        return 0

    return max(map(lambda p: run_plan(bp, robots.copy(), p, resources.copy(), time_left, max_cost), possibilities))


def calc_blueprint_quality(bp):
    global cur_best

    robots = [1, 0, 0, 0]
    resources = [0, 0, 0, 0]
    cur_best = 0
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
for i, bp in enumerate(blueprints):
    print(f'running bp {i+1} for {RUNTIME} minutes @ {datetime.datetime.now()} ')
    best_by_minute = dict()
    cur_best = 0
    qualis.append(calc_blueprint_quality(bp))
    print(f'max {qualis[-1]}')

print(sum([((i + 1) * v) for i, v in enumerate(qualis)]))
print(qualis)
print('962 too low')
print(datetime.datetime.now() - begin_time)
