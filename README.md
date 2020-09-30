# CS490_Project1
## This is the first project the CS 490 of which the purpose is to currently dyanmically display tweets pertaining to a paticular food recipe


### Languages used:
python

html

css


### APIs used:
twitter API

tweepy

flask

spoonacular



### USING THE TWITTER API

First need to make a twitter account IF YOU DONT ALREADY HAVE ONE here:
https://twitter.com

Next you need to apply for a developer account if you have not already done so:
https://developer.twitter.com/en/apply-for-access

Next Fill out the Application and create a new project

The website will then take you to your dashboard
![Image of instlling tweepy](https://github.com/gamblinflanagan/CS490_Project1/issues/3#issue-706764966)

If your keys are not displayed click the view Keys button
![Image of instlling tweepy](https://github.com/gamblinflanagan/CS490_Project1/issues/4#issue-706765206)

copy and add keys to the code save the keys in a discrete location

create a .env file copy this code and add the correct keys to each line

* export TWEEPY_CONSUMER_KEY='API KEY'

* export TWEEPY_CONSUMER_SECRET='SECRET API KEY'

* export TWEEPY_ACCESS_TOKEN='ACCESS TOKEN'

* export TWEEPY_ACCESS_TOKEN_SECRET='ACCESS SECRET TOKEN'

type in the command line source filename.env

if for some reason you need to access your keys again after clsing the page go back to apply for a developer page click the aply button and you will be logged back into your account




### INSTALLING PIP
pip or any up to date de facto standard package-managment system will be needed for the next APIs (flask, tweepy)
PIP is recommended

INSTRUCTIONS ON HOW TO DOWNLOAD PIP HERE - https://pip.pypa.io/en/stable/installing/




### INSTALLING FLASK

in your working directory write the following: "sudo pip install flask"


you should see the following:
![Image of instlling tweepy](https://github.com/gamblinflanagan/CS490_Project1/issues/1#issue-706760852)


### INSTALLING TWEEPY

in your working directory write the following: "sudo pip install tweepy"

you should see the following:
![Image of instlling tweepy](https://github.com/gamblinflanagan/CS490_Project1/issues/2#issue-706760938)


### INSTALLING SPOONACULAR

In your working directory write the following: "sudo pip install spoonacular"
![Image of instlling spoonacular](https://github.com/gamblinflanagan/CS490_Project1-jcf29/blob/master/Images/install_spoonacular.png)

Next need to make a twitter account IF YOU DONT ALREADY HAVE ONE here:
https://spoonacular.com/api/docs/recipes-api

Go to your spoonacular dashboard (you will be brouht here after your account is created)

Click on Profile and then show API Key and your api key will be displayed

copy and add keys to the code save the keys in a discrete location

create a .env file copy this code and add the correct keys to each line

export SPOONACULAR_API_KEY='API KEY'
