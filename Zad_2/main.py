import json
import requests
import pandas as pd
import numpy as np 
from math import *
from pandas import json_normalize

def getJsons(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as connError:
        print ("Connection error: ", connError)
    except requests.exceptions.ConnectTimeout as timeOut:
        print("Timeout: ", timeOut)
    return response

def changeKey(jsonFile, usersKey, postsKey):
    for i in jsonFile:
        i[postsKey] = i.pop(usersKey)
    return  jsonFile

def mergeJson(usersFile, postsFile, usersKey, postsKey):
    #We need to change keyName for users in usersJson
    for i in usersFile:
        for j in postsFile:
            if i[usersKey] == j[postsKey]:
                i.update(j)
    return usersFile

#Count posts writen by users
def countPosts(jsonFile):
    totalPosts = {}
    for i in jsonFile:
        if i['username'] in totalPosts:
            totalPosts[i['username']] += 1
        else:
            totalPosts[i['username']] = 1
    return totalPosts

def uniquePosts(postsJson):
    postsDf = pd.DataFrame(postsJson)
    unique = postsDf[postsDf['title'].duplicated()]
    if unique.empty:
        return "All posts have unique titles"
    return unique


##Haversine formula
def haversineForm(lat1, lon1, lat2, lon2):
    earthRadius = 6371.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lon2, lat2 = map(np.radians, [lon2, lat2])

    #difference between two latlons
    lat3 = lat2 - lat1
    lon3 = lon2 - lon1
    a = np.sin(lat3 / 2.0) ** 2 + cos(lat1) * np.cos(lat2) * np.sin(lon3 / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    haversine = earthRadius * c
    return haversine

def nearest(userDataFrame):
    userDataFrame = userDataFrame.filter(['id', 'username', 'address.geo.lat', 'address.geo.lng'])
    userDataFrame['address.geo.lat'] = pd.to_numeric(userDataFrame['address.geo.lat'])
    userDataFrame['address.geo.lng'] = pd.to_numeric(userDataFrame['address.geo.lng'])
    users = {}
    for i in range(len(userDataFrame)):
        distance = haversineForm(userDataFrame.iat[i, 2], userDataFrame.iat[i, 3],
                                           userDataFrame['address.geo.lat'], userDataFrame['address.geo.lng'])
        minDistance = distance[distance > 0].idxmin()
        users.update({userDataFrame.iat[i, 1]: userDataFrame.iat[minDistance, 1]})
    return users

def main():
    responseFromUsers = getJsons("https://jsonplaceholder.typicode.com/users")
    responseFromPosts = getJsons("https://jsonplaceholder.typicode.com/posts")

    usersJson = json.loads(responseFromUsers.text)
    postsJson = json.loads(responseFromPosts.text)

    changeKey(postsJson, "id", "userId")

    print(mergeJson(usersJson, postsJson, "id", "userId"))

    countedPosts = countPosts(mergeJson(usersJson, postsJson, "id", "userId"))

    print(countedPosts)

    print(uniquePosts(postsJson))

    nearestUsers = nearest(json_normalize(usersJson))
    for i, j in nearestUsers.items():
        print("Najblizszym sasiadem {0} jest {1}".format(i,j))

if __name__ == '__main__':
    main()