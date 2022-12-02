import datetime

begin_time = datetime.datetime.now()

_, ROCK, PAPER, SCISSORS = range(4)
POINTS = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}
LOOSE, DRAW, WIN = ('X', 'Y', 'Z')

with open('./input.txt') as f:
    score = 0
    while line := f.readline().rstrip():
        opp_shape, outcome = line.split(' ')
        opp_score = POINTS[opp_shape]

        if outcome == LOOSE:
            if opp_score == ROCK: my_score = SCISSORS
            if opp_score == SCISSORS: my_score = PAPER
            if opp_score == PAPER: my_score = ROCK
        elif outcome == DRAW:
            my_score = opp_score
            score += 3
        elif outcome == WIN:
            score += 6
            if opp_score == SCISSORS: my_score = ROCK
            if opp_score == PAPER: my_score = SCISSORS
            if opp_score == ROCK: my_score = PAPER

        score += my_score

print(score)
print(datetime.datetime.now() - begin_time)
