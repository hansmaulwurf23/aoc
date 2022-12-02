import datetime

begin_time = datetime.datetime.now()

_, ROCK, PAPER, SCISSORS = range(4)
POINTS = {'A': ROCK, 'B': PAPER, 'C': SCISSORS,
          'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}
WIN, DRAW = (6, 3)
score = 0

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        shapes = line.split(' ')
        opp_score, my_score = POINTS[shapes[0]], POINTS[shapes[1]]
        score += my_score
        if opp_score == my_score:
            score += DRAW
        else:
            if (my_score == ROCK and opp_score == SCISSORS) or \
               (my_score == SCISSORS and opp_score == PAPER) or \
               (my_score == PAPER and opp_score == ROCK):
                score += WIN

print(score)
print(datetime.datetime.now() - begin_time)
