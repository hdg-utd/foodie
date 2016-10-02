"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib
from flask import Flask, request, jsonify

def googleJSON(queryGoogle):

    #Data to be sent
    api_key = 'AIzaSyDAYy8QGPiHtCw42sRNkeJft59ls1SxI68'
    query = queryGoogle.lower()

    #API Url
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
        'limit': 1,
    }

    #Sending the request
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    count = 0

    #Empty list to be appended to insert strings of results
    # 0)Name
    # 1)Google URL
    googleList = []

    for element in response['itemListElement']:
        if count == 1:
            break
        #print element['result']['name'] + ' (' + element['result']['image']['contentUrl'] + ')'
        googleList.append(element['result']['name'])
        googleList.append(element['result']['image']['contentUrl'])
        count += 1

    return googleList

def dDJSON(queryDD):

    #Data to be sent
    query = queryDD.replace(" ", "%20").lower()

    #API Url
    service_url = 'http://api.duckduckgo.com/?q={}&format=json&skip_disambig=1'.format(query)

    #Sending the request
    url = service_url
    response = json.loads(urllib.urlopen(url).read())

    #Empty list to be appended to insert strings of results
    # 0)Country of Origin
    # 1)Ingredients
    dDList = []

    count = 0

    for element in response['Infobox']['content']:

        if('origin' in element['label']):
            dDList.append(element['value'])
        if('Main ingredient' in element['label']):
            dDList.append(element['value'])
        
    return dDList

#Return Combined List
def jsonLister(queryString):

    mainList_1 = []

    #Google
    try:
        mainList_1 = googleJSON(queryString)
        print "Yes GG"
    except:
        print "No GG"

    try:
        mainList_2 = dDJSON(queryString)

        for items in mainList_2:
            mainList_1.append(items)

        print "Yes DD"

        listOfMeats = ['chicken', 'ham', 'meat', 'turkey', 'beef', 'pork', 'salami']

        item1Counter = 0

        for item1 in listOfMeats:
            if item1 in mainList_1[3].lower():
                mainList_1.append('no')
                break
            if item1Counter == 6:
                mainList_1.append('yes')
                break
    
        item1Counter += 1
    except:
        print "No DD"
    

    return mainList_1


#Return combined dictionary
def jsonDict(inputList):
    
    count = 0

    jsonDictionary = {}

    for items in inputList:
        if count == 0:
            jsonDictionary.update({'name': '{}'.format(items)})
            count += 1
            continue
        if count == 1:
            jsonDictionary.update({'imgURL': '{}'.format(items)})
            count += 1
            continue
        if count == 2:
            jsonDictionary.update({'origin': '{}'.format(items)})
            count += 1
            continue
        if count == 3:
            jsonDictionary.update({'ingredients': '{}'.format(items)})
            count += 1
            continue
        if count == 4:
            jsonDictionary.update({'vegetarian': '{}'.format(items)})
            count += 1
            continue

    return jsonDictionary

def mainToRun(queryFinal):
    return jsonDict(jsonLister(queryFinal))


app = Flask(__name__)

@app.route('/<string:query>', methods=['GET'])
def index(query):
    return jsonify(mainToRun(query))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
