data = []
with open('check.txt', 'r') as f:
    for line in f:
        data.append(line.replace('\n', ''))

money = 1
line = data[0].split(',')
money_player = int(line[4]) + money
line[4] = str(money_player)
ready_line = ",".join(line)
data[0] = ready_line

f = open("check.txt", 'w')
for line in data:
    f.write(line + '\n')
f.close()



