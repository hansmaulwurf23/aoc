c = 1
a, b, d = 1, 1, (26 if c == 0 else 33)


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)


while d:
    print(a)
    c = a
    a += b
    b = c
    d -= 1

print(a)
print(fib(35))
a += 11 * 18

print(a)
