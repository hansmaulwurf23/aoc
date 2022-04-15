import datetime

begin_time = datetime.datetime.now()
FWD = 303

ins_pos = 0
target = 0
runs = 50000000
buf_len = 0
while buf_len < runs:
    if ins_pos == 1:
        target = buf_len
    inserts = (buf_len - ins_pos) // FWD
    buf_len += (inserts + 1)
    ins_pos = (ins_pos + (inserts + 1) * (FWD + 1) - 1) % buf_len + 1

print(target)
print(datetime.datetime.now() - begin_time)
