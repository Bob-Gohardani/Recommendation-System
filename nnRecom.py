import csv
import random
import math
import operator
import numpy as np

DataSet = {}
movies = {}
validation_sets = []
training_sets = []


# Data Normalization:
with open("movies_1.csv", 'rb') as myfile:
    reader = csv.reader(myfile)
    for row in reader:
        x = [float(y) for y in row[1:]]
        movies[row[0]] = x

dct = {}
for i in range(4):
    dct[i] = []

for k, v in movies.iteritems():
    for j in range(4):
        dct[j].append(v[j])

for key in dct:
    high = max(dct[key])
    low = min(dct[key])
    dct[key] = []
    dct[key].append(low)
    dct[key].append(high)

for k, v in movies.iteritems():
    for i in range(len(v)):
        i = int(i)
        y = (2 * (v[i] - dct[i][0]) / (dct[i][1] - dct[i][0])) - 1
        movies[k][i] = y

# download data from different csv files and mix them together in dataset
with open('train.csv', 'rb') as f:
    reader = csv.reader(f)
    l1 = list(reader)


for l in l1:
    N = [float(x) for x in l[0].split(';')]
    features = movies[str(int(N[2]))]
    for j in features:
        N.append(float(j))

    if str(int(N[1])) not in DataSet.keys():
        DataSet[str(int(N[1]))] = [N[2:]]
    else:
        DataSet[str(int(N[1]))].append(N[2:])

#looping through k from 1 to 10 to find proper neighbourhood:
def euclideanDistance(inst1, inst2):
    distance = 0
    for x in range(2,6):
        distance += pow((inst1[x] - inst2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
    # find K closest neighbors
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# get averge of rating of neighbours
def getResponse(neighbors):
	sum = 0
	for x in range(len(neighbors)):
		sum += neighbors[x][1]
	return round(sum / len(neighbors))

def getErrorRate(testSet, predictions):
    sum = 0
    for x in range(len(testSet)):
        sum = abs(float(testSet[x][1]) - predictions[x])
	return (sum/float(len(testSet)))

errors_hyper = []

for k in range(1, 10):
    error_set = []
    for key in DataSet.keys():
    	predictions=[]
        person1 = DataSet[key]
        trainingSet = []
        testSet = []
        for i in range(int(len(person1)/10)):
            x = person1[random.randint(0, len(person1)-1)]
            testSet.append(x)
            person1.remove(x)
        trainingSet = person1

    	for x in range(len(testSet)):
    		neighbors = getNeighbors(trainingSet, testSet[x], k)
    		result = getResponse(neighbors)
    		predictions.append(result)

    	error = getErrorRate(testSet, predictions)
        error_set.append(error)
        errors_hyper.append((k,sum(error_set)/len(error_set)))

final_k = min(errors_hyper, key = lambda t: t[1])[0]



with open('task.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
list_1 = []

for l in your_list:
    N = [x for x in l[0].split(';')]
    user_data = DataSet[N[1]]  # all train data relating to this user
    movie_info = movies[N[2]]  # features related to this movie
    movie_info = [1,1]+movie_info
    neighbors = getNeighbors(user_data, movie_info, final_k)
    result = getResponse(neighbors)
    N[3] = int(result)
    list_1.append(N)

with open("submission.csv", 'wb') as myfile:
    wr = csv.writer(myfile, delimiter=';')
    for l in list_1:
        wr.writerow(l)
