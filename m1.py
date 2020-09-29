from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import tweepy
import sys
import os
import flask 
import random
import requests
from requests.exceptions import HTTPError
import spoonacular as sp
import json


''' These Keys are needed to access twitters developer API, the values are stored in another file as they are confidential '''
consumer_key = os.environ['TWEEPY_CONSUMER_KEY']
consumer_secret = os.environ['TWEEPY_CONSUMER_SECRET']
access_token = os.environ['TWEEPY_ACCESS_TOKEN']
access_token_secret = os.environ['TWEEPY_ACCESS_TOKEN_SECRET']

''' This Keys is needed to access spoonacular API, the value is stored in another file as it is confidential '''
spoonacular_key = os.environ['SPOONACULAR_API_KEY']



''' This Funcion uses the tweepy API to dynamically pulls tweets from twitter with a paticular hashtag '''
def GetTweets(theTag):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #authenticates twitter keys
    auth.set_access_token(access_token, access_token_secret)  #authenticates twitter access token
    api = tweepy.API(auth)
    
    rst = ""
    counter = 0
    maxx = random.randint(1, 10)
    
    for tweet in tweepy.Cursor(api.search,q=theTag,      
                            count=maxx,                  #max number of tweets to pull
                            lang="en",                   #excludes tweets not in english language
                            tweet_mode = 'extended',     #takes full tweet instead of first 140 characters
                            since="2020-01-01").items(): #will only pull tweets as far back as specified date
        rTime = str(tweet.created_at) #gets time tweet was created
        rText = str(tweet.full_text)  #gets the full tweet itself
        counter += 1
        rst = rText+"\n"+rTime+"\n\n"
        if counter == maxx: #if the maximum number of tweets was pulled
            break
    return rst
    

 
def Recipe(URL, plate):
    rtlst = []
    ingrds = ""
    ident = ""
    
    response = requests.get(URL)
    response.encoding = 'utf-8'
    text = response.text
    json_response = json.loads(text)
    
    #count = 0
    for result in json_response['results']:
        ident = str(result['id'])
        title = str(result['title'])
        img = str(result['image'])
        if plate in title:
            rtlst.append(title)
            rtlst.append(img)
            break
        #count +=1
    
    URL = "https://api.spoonacular.com/recipes/"+ident+"/ingredientWidget.json"+"?apiKey="+spoonacular_key
    response = requests.get(URL)
    response.encoding = 'utf-8'
    text = response.text
    json_response = json.loads(text)
    
    for i in json_response['ingredients']:
        name = str(i['name'])
        if name not in ingrds:
            ingrds += name+"\n"
    rtlst.append(ingrds)
    
    
    return rtlst    




tagnum = random.randint(0, 6)
taglst = ["Gorgonzola", "pancakes", "steak", "chickenparm", "frenchtoast", "cinnamonbon", "calzone"] #list of hastags to search
foodlst = ["Pasta-With-Gorgonzola-Sauce", "Pancakes", "Flank-Steak-with-Mushroom-Sauce", "Chicken-Wings", "Pumpkin-French-Toast", "Cinnamon-Rolls", "Sausage Calzone"]





dish = str(foodlst[tagnum])
url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey='+spoonacular_key+'&query='+dish
dish = dish.replace("-", " ")
resLst = Recipe(url, dish)
name = str(resLst[0])
image = str(resLst[1])
ingd = str(resLst[2])
print(name+"\n"+image+"\n"+ingd)




tag=str("#"+taglst[tagnum])               #holds a string value which is the hashtag that GetTweets will use picked at random based on value of tagnum
quote = str(GetTweets(tag))      #string that holds the return value (which is a tweet) from GetTweets
print(quote)

    
    

''' This Function creates the front end portion of the web application '''
app = flask.Flask(__name__)
@app.route('/') # Python decorator
def index():
    print("reached index method")
    
    return flask.render_template(
        "index.html",           #html file to render the front end portion of the web app
        twitter_quote = quote   #sets value of tweet to be displayed to tweet pulled in previous function
        )

app.run(
    port=int(os.getenv('PORT', 8080)),  #specifies what port to run on
    host=os.getenv('IP', '0.0.0.0'),    #specifies what ip to run on
    #debug=True                          #run in debug mode
)
