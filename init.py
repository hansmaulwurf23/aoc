# downloads the input of the current day (as input.txt) and making sure that ./<year>/<day>/ folder exists.
import datetime
import os.path
from urllib import request

now = datetime.datetime.now()
year, day = now.year, now.day
with open('./cookie') as f:
    cookie = f.readline()

if not os.path.exists(f'./{year}/day {day:02d}'):
    os.makedirs(f'./{year}/day {day:02d}')

if os.path.exists(f'./{year}/day {day:02d}/input.txt'):
    print('Input exists. Skipping.')
    exit(0)

req = request.Request(f'https://adventofcode.com/{year}/day/{day}/input', headers={'cookie': cookie})
with request.urlopen(req) as f:
    with open(f'./{year}/day {day:02d}/input.txt', 'w') as inp:
        inp.write(f.read().decode('utf-8'))
    print('downloaded and saved.')
