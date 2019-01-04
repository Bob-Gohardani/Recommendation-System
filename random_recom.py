import csv
import random
with open('task.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
list_1 = []
for l in your_list:
    N = [x for x in l[0].split(';')]
    N[3] = random.randint(1,5)
    list_1.append(N)

with open("submission.csv", 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=';')
    for l in list_1:
        wr.writerow(l)
