a = 12
b = a - 1
while b > 1:
    a *= b
    b -= 1

c = 77
d = 87

a += (77 * 87)

# output on my breathtakingly fast 23 minute basic implementation:
# TOOGLE 25 from ['inc', 'c'] to dec
# TOOGLE 23 from ['inc', 'd'] to dec
# TOOGLE 21 from ['jnz', '87 d'] to cpy
# TOOGLE 19 from ['jnz', '1 c'] to cpy
# -> while loop in line 3 is exited after TOGGLE 19

# 479008299