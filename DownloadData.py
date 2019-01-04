import csv
import random
import math
import operator
import requests
movies = {}



#downloading data from API:

api_key = "24370f953f5f3f70890d54a4705b8ff4"

with open('movies.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        resp = requests.get("https://api.themoviedb.org/3/movie/"+ row[1] +"?api_key="+api_key)
        json_resp = resp.json()
        # Here I only use the first genre of each movie mentioned
        movies[row[0]] = [
                          str(row[0]),
                          str(json_resp["budget"]),
                          str(json_resp["genres"][0]["id"]),
                          str(json_resp["runtime"]),
                          str(json_resp["release_date"].split('-')[0]),
                         ]

with open("movies_1.csv", 'wb') as myfile:
    wr = csv.writer(myfile)
    for key, value in movies.iteritems():
        wr.writerow(value)
