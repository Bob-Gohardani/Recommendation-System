import csv
import random
import math
import operator
import numpy as np


DataSet = {}
listSet = []

with open('train.csv', 'rb') as f:
    reader = csv.reader(f)
    l1 = list(reader)


for l in l1:
    N = [int(x) for x in l[0].split(';')]

    if str(int(N[1])) not in DataSet.keys():
        DataSet[str(int(N[1]))] = [N[1:]]
    else:
        DataSet[str(int(N[1]))].append(N[1:])
    listSet.append(N[1:])

# [0 :'USERID', 1 :'MOVIEID', 2 :'MOVIE_RATING']
# find similar users that have already rated this movie:
def findSimilar(userID, Data, k, movieID):
    user = DataSet[str(userID)]

    # if user has same rating for almost all movies then he will probably have same one for this movie:
    variance = np.var([x[2] for x in user])
    if variance <= 0.6:
        return sum([x[2] for x in user]) / float(len(user))

    similar = []
    user_avg = sum([x[2] for x in user]) / float(len(user))
    for key, v in DataSet.iteritems():
        containsMovie = any(int(movieID) == int(x[1]) for x in v)
        variance1 = np.var([x[2] for x in v])
        if (key != userID) and containsMovie and (variance1 > 1):
                avg = sum([x[2] for x in v]) / float(len(v))
                up = 0
                temp1 = []
                temp2 = []
                for item in user:
                    for item2 in v:
                        if item[1] == item2[1]:
                            up += (item2[2] - avg)*(item[2] - user_avg)

                            temp1.append(item[2])
                            temp2.append(item2[2])
                            break
                sum1 = 0
                sum2 = 0

                # for current user
                for num in temp1:
                    sum1 += (num - user_avg)**2

                # for all neighbours
                for num in temp2:
                    sum2 += (num - avg)**2

                down = (sum1**0.5)*(sum2**0.5)

                similarity = up / down
                similar.append((key,similarity))

    similar = sorted(similar, key=lambda x: x[1], reverse=True)
    similar = similar[:k]
    # rate movie based on what other users said about that movie
    l1 = []
    for tuple in similar:
        neighbour_data = DataSet[str(tuple[0])]
        for x in neighbour_data:
            if int(x[1]) == int(movieID):
                l1.append([x[2], tuple[1]])
                break

    down1 = sum([x[1] for x in l1])
    up1 = sum([x[0]*x[1] for x in l1])
    return round(float(up1)/down1)





error_set = []
for k in range(2, 10):
    testSet = []
    #list = DataSet.keys()
    data_temp = DataSet.copy()

    for i in range(int(len(data_temp)/20)):
        x = data_temp[str(random.choice(data_temp.keys()))]
        testSet.append(x)
        del data_temp[str(x[0][0])]

    user_error = []
    for user in testSet:
        temp = [] # errors of all movies of a single user
        for rating in user:
            rate_guess = findSimilar(user[0][0], data_temp, k, rating[1])
            temp.append(abs(rating[2] - rate_guess))
        user_error.append(sum(temp)/len(user))

    error_set.append([k, sum(user_error)/len(user_error)])

final_k = min(error_set, key = lambda t: t[1])[0]


with open('task.csv', 'rb') as g:
    reader1 = csv.reader(g)
    your_list = list(reader1)

list_1 = []
for l in your_list:
    N = [x for x in l[0].split(';')]
    user = DataSet[str(N[1])]
    rate_guess = findSimilar(user[0][0], DataSet, final_k, N[2])
    N[3] = int(rate_guess)
    list_1.append(N)

with open("submission.csv", 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=';')
    for l in list_1:
        wr.writerow(l)
