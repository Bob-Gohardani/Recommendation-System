import csv
import random
import math
import operator
import numpy as np


DataSet = {} # for users
DataSet2 = {} # for movies
relations = []
relations = {}
with open('train.csv', 'rb') as f:
    reader = csv.reader(f)
    l1 = list(reader)

for l in l1:
    N = [int(x) for x in l[0].split(';')]

    if str(int(N[1])) not in DataSet.keys():
        DataSet[str(int(N[1]))] = [N[1:]]
    else:
        DataSet[str(int(N[1]))].append(N[1:])

    if str(int(N[2])) not in DataSet2:
        DataSet2[str(int(N[2]))] = [[N[1], N[3]]]
    else:
        DataSet2[str(int(N[2]))].append([N[1], N[3]])


def movieRelation():
    for k, v in DataSet2.iteritems():
        # averge rating of the movie among all users
        movie_avg =  sum(x[1] for x in v) / float(len(v))
        relations[k] = []
        for key, value in DataSet2.iteritems():
            up = 0
            temp1 = []
            temp2 = []

            if key != k:
                other_avg =  sum(x[1] for x in value)/ float(len(value))
                for item1 in v:
                    for item2 in value:
                        if (item1[0] == item2[0]) and (item1[1] !=0 or item2[1] != 0):
                            up += (item1[1]-movie_avg) * (item2[1] - other_avg)
                      
                            temp1.append(item1[1])
                            temp2.append(item2[1])
                            break

                sum1 = 0
                sum2 = 0
                for num in temp1:
                    sum1+=(num - movie_avg)**2
                for num in temp2:
                    sum2+= (num - other_avg)**2
                down = (sum1**0.5)*(sum2**0.5)
                rel = float(up) / down
                relations[k].append((key, rel))

movieRelation()


def findSimilar(userID, k, movieID):
    user = DataSet[str(userID)]

    # if user has same rating for almost all movies then he will probably have same one for this movie:
    variance = np.var([x[2] for x in user])
    if variance <= 0.6:
        return sum([x[2] for x in user]) / float(len(user))

    # find k closet movies from this user's ratings
    similar = relations[str(movieID)]
    similar = sorted(similar, key=lambda x : x[1], reverse=True)
    similar = similar[:k]
    down1 = 0.01
    up1 = 0
    for tuple in similar:
        l = DataSet[str(userID)]
        for x in l:
            if int(x[1]) == int(tuple[0]):
                down1 += abs(tuple[1])
                up1 += tuple[1] * x[2]
                break
    return round(float(up1)/ down1)




error_set = []
for k in range(2, 15):
    testSet = []
    data_temp = DataSet.copy()

    for i in range(int(len(data_temp)/10)):
        x = data_temp[str(random.choice(data_temp.keys()))]
        testSet.append(x)
        del data_temp[str(x[0][0])]

    user_error = []
    for user in testSet:
        temp = [] # errors of all movies of a single user
        for rating in user:
            rate_guess = findSimilar(user[0][0], k, rating[1])
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

    rate_guess = findSimilar(user[0][0], final_k, N[2])
    N[3] = int(rate_guess)
    list_1.append(N)

with open("submission.csv", 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=';')
    for l in list_1:
        wr.writerow(l)
