# downloads the input of the current day (as input.txt) and making sure that ./<year>/<day>/ folder exists.
import datetime
import os.path
import sys
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

if len(sys.argv) > 1:
    now = datetime.datetime.strptime(f'{sys.argv[1]}-12-{sys.argv[2]}', '%Y-%m-%d')
else:
    now = datetime.datetime.now()

year, day = now.year, now.day
with open('./cookie') as f:
    cookie = f.readline()

if not os.path.exists(f'./{year}/day {day:02d}'):
    os.makedirs(f'./{year}/day {day:02d}')

if os.path.exists(f'./{year}/day {day:02d}/input.txt'):
    print(f'{year}/{day} Input exists. Skipping.')
else:
    req = request.Request(f'https://adventofcode.com/{year}/day/{day}/input', headers={'cookie': cookie})
    try:
        with request.urlopen(req) as f:
            with open(f'./{year}/day {day:02d}/input.txt', 'w') as inp:
                inp.write(f.read().decode('utf-8'))
            print('downloaded and saved.')
    except HTTPError as e:
        print(f'HTTP Error: {e.code} {e.reason}')
        exit(1)

req = request.Request(f'https://adventofcode.com/{year}/day/{day}', headers={'cookie': cookie})
with request.urlopen(req) as f:
    h = f.read().decode('utf-8')
    soup = BeautifulSoup(h, 'html.parser')
    for i, pre in enumerate(soup.find_all('pre')):
        fname = f'./{year}/day {day:02d}/code{i:02d}.txt'
        print(f'writing {fname}...')
        with open(fname, 'a') as c:
            c.write(pre.text)
