import json
import requests
import pandas as pd

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
if __name__ == '__main__':
    main()