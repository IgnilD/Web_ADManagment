import os
import datetime

now = datetime.datetime.now()
current_data = now.strftime("%d.%m.%Y")

current_day = now.day
current_month = now.month
current_year = now.year


with open(file="start_data.txt", mode="r") as start_file:
    start_data = start_file.readlines()

with open(file="fin_data.txt", mode="r") as fin_file:
    fin_data = fin_file.readlines()

print(start_data)
print(fin_data)


modified_start_data = []
for data in start_data:
    datas = data.strip("\n").split("|")
    user_to_block = datas[0]
    date_to_block = datas[1].split(".")
    print(date_to_block)
    if int(date_to_block[0]) <= current_day and int(date_to_block[1]) <= current_month and int(date_to_block[2]) <= current_year:
        os.system(f"net user {user_to_block} /active:no")
        if len(datas) == 3:
            description_to_block = datas[2]
            os.system(f'net user {user_to_block} /comment:"{description_to_block}"')

        modified_start_data.append(data)


modified_fin_data = []

for data2 in fin_data:
    datas = data2.strip("\n").strip(" ").split("|")
    user_to_unblock = datas[0]
    date_to_block = datas[1].split(".")
    print(date_to_block)
    if int(date_to_block[0]) + 1 <= current_day and int(date_to_block[1]) <= current_month and int(date_to_block[2]) <= current_year:
        os.system(f"net user {user_to_unblock} /active:yes")
        os.system(f'net user {user_to_unblock} /comment:""')

        modified_fin_data.append(data2)


for s in modified_start_data:
    start_data.remove(s)
start_data = ''.join(str(e) for e in start_data)


for f in modified_fin_data:
    fin_data.remove(f)
fin_data = ''.join(str(e) for e in fin_data)


with open(file="start_data.txt", mode="w") as start_file:
    start_file.write(start_data)


with open(file="fin_data.txt", mode="w") as fin_file:
    fin_file.write(fin_data)
