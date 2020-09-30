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
    

''' This Function uses the spoonacular api and requests library to get the recipe and recipe information ''' 
def Recipe(URL, plate):
    rtlst = []   #conatins recipe and recipie information
    ingrds = []  #list of ingredients
    ident = ""   #recipie id number
    
    response = requests.get(URL)     #gets response code from given url
    response.encoding = 'utf-8'
    text = response.text             #gets content from response
    json_response = json.loads(text) #puts content in json format
    
    #count = 0
    for result in json_response['results']: 
        ident = str(result['id'])       #id of recipie
        title = str(result['title'])    #name of recipie
        img = str(result['image'])      #picture of recipie
        if plate in title:
            rtlst.append(title)
            rtlst.append(img)
            break
        #count +=1
    
    URL = "https://api.spoonacular.com/recipes/"+ident+"/priceBreakdownWidget.json"+"?apiKey="+spoonacular_key  #url for recipe info
    response = requests.get(URL)
    response.encoding = 'utf-8'
    text = response.text
    json_response = json.loads(text)
    
    for i in json_response['ingredients']:
        name = str(i['name'])                     #ingreident name
        unit = str(i['amount'] ['us'] ['unit'])   #unit of measurement
        value = str(i['amount'] ['us'] ['value']) #amount of ingreident 
        indg = value+unit+" "+name
        if indg not in ingrds:
            ingrds.append(indg)
    rtlst.append(ingrds)
    
    return rtlst    




tagnum = random.randint(0, 6)
taglst = ["Gorgonzola", "pancakes", "steak", "Chickenwings", "frenchtoast", "Cinnamonrolls", "calzone"] #list of hastags to search
foodlst = ["Pasta-With-Gorgonzola-Sauce", "Pancakes", "Flank-Steak-with-Mushroom-Sauce", "Chicken-Wings", "Pumpkin-French-Toast", "Cinnamon-Rolls", "Sausage Calzone"]
#list of foods for spoonacualr to search




dish = str(foodlst[tagnum])                                                                      #holds string value of recipie that Recipe will return
url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey='+spoonacular_key+'&query='+dish #url for recipe
furl = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=APIKEY&query'+dish              #url to be displayed on web page
dish = dish.replace("-", " ")                                                                    #recipe name used in function Recipe
resLst = Recipe(url, dish)  #list containing recipe and information
name = str(resLst[0])       #name of recipe
image = str(resLst[1])      #image of recipe
ingd = resLst[2]            #ingredients list
print(name+"\n"+image+"\n"+str(ingd)+"\n"+furl)




tag = str("#"+taglst[tagnum])      #holds a string value which is the hashtag that GetTweets will use picked at random based on value of tagnum
quote = str(GetTweets(tag))        #string that holds the return value (which is a tweet) from GetTweets
print(quote)

    
    

''' This Function creates the front end portion of the web application '''
app = flask.Flask(__name__)
@app.route('/') # Python decorator
def index():
    print("reached index method")
    
    return flask.render_template(
        "index.html",                       #html file to render the front end portion of the web app
        twitter_quote = quote,              #sets value of tweet to be displayed to tweet pulled in previous function
        the_name = name,                    #sets value of recipe name to be displayed to recipe name pulled in previous function
        the_image = image,                  #sets value of recipe image to be displayed to recipe image pulled in previous function
        len = len(ingd), ingd = ingd,       #sets value of ingredients to be displayed to ingredients pulled in previous function
        the_furl = furl                     #sets value of url to be displayed to recipe url 
        )

app.run(
    port=int(os.getenv('PORT', 8080)),  #specifies what port to run on
    host=os.getenv('IP', '0.0.0.0'),    #specifies what ip to run on
    #debug=True                          #run in debug mode
)



#<link