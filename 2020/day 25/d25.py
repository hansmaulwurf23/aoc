import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as file:
    pub_keys = list(map(int, file.readlines()))


# just use one of them
pub_key = pub_keys[0]
loop_size = 0
subject_number = 7
value = subject_number
while value != pub_key:
    value = (value * subject_number) % 20201227
    loop_size += 1

subject_number = pub_keys[1]
value = subject_number
for i in range(loop_size):
    value = (value * subject_number) % 20201227

print(value)
print(datetime.datetime.now() - begin_time)
