import functools
import datetime

begin_time = datetime.datetime.now()
d = 26

@functools.cache
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

print(f'part 1 {fib(d + 2) + 11 * 18}')
print(f'part 1 {fib(d + 7 + 2) + 11 * 18}')
print(datetime.datetime.now() - begin_time)
