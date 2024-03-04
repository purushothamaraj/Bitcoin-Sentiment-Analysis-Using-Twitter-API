import tweepy as twp
from textblob import TextBlob

from dotenv import load_dotenv
import os
from matplotlib import pyplot as plt
import numpy as np


load_dotenv()

#consumer keys
API_KEY = "4084w6OgZgpfCPokKiptoOu0d"
API_KEY_SECRET = "0hoOMwSSWtk1A3MpEz8DnvHldwBeQILWHPAKH3urzqeM1NXbRA"
#other
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACofVQEAAAAA37oDeWUoJjHHjFGcZIB7Hczsxbw%3Dq9faBKvvgAcnkTycCSEg0VnzkloiQJMmGNhBQFRiwYOrwgcaIw"
ACCESS_TOKEN = "1454477188669923332-emJUzrZpc7De5Oe8VjV4WFc2hcKN33"
ACCESS_TOKEN_SECRET = "O5kSDeMZMyxTfEcSTSe6ySOSog3tSio4NO3q0Ud3HQxi0"

likesArray = list()
positiveCount= 0.0
negativeCount=0.0
neutralCount=0.0
sentiment = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']

auth = twp.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = twp.API(auth)

def getPolarity(tweet):
    #return TextBlob.sentiments.(tweet)
    return TextBlob(tweet).sentiment.polarity


def getSentiment(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'


def find_account_value(tweet):
    #check verification
    #check followers
    value = 1
    ver = tweet.user.verified
    if(ver == True):
        value *= 1.10
    elif(tweet.user.followers_count > 100000):
        value *= 1.05
    else:
        value += 0.05
    return value


#Fids value/impact of a single tweet
#param: tweet - item: full item of all data regarding current tweet
#param: list_of_tweets - int: a full list of tweets with all information regarding likes, user, retweets, etc.
def find_tweet_value(list_of_tweets, tweet):

    # getting tweet_likes
    tweet_likes = tweet.favorite_count
    tweet_rts = tweet.retweet_count

    #calculating averages
    total_likes = 0
    total_rts = 0
    for tweet in list_of_tweets:
        total_likes += tweet.favorite_count
        total_rts += tweet.retweet_count

    avg_likes = total_likes / len(list_of_tweets)
    avg_rts = total_rts / len(list_of_tweets)

    #initializing value
    value = 5
    
    #checking likes alt
    if tweet_likes > avg_likes:
        value += tweet_likes / avg_likes
    elif tweet_likes < avg_likes:
        value -= tweet_likes / avg_likes

    #checking retweets
    if tweet_rts > avg_rts:
        value += tweet_rts / avg_rts
    elif tweet_rts < avg_rts:
        value -= tweet_rts / avg_rts

    
    return value


def getMagnitude(list_of_tweets, tweet):
    pol = getPolarity(tweet.text)
    sen = getSentiment(pol)

    mag = 0

    if(sen == "Negative"):
        mag = find_account_value(tweet) + find_tweet_value(list_of_tweets, tweet) * -1
    elif(sen == "Neutral"):
        mag = 0
    else:
        mag = find_account_value(tweet) + find_tweet_value(list_of_tweets, tweet)
    
    return mag


def getConnotation(list_of_tweets):
    con = 0
    for tweet in list_of_tweets:
        con += getMagnitude(list_of_tweets, tweet)
    return con


#loops through tweets and prints all information regarding tweet
#param: list_of_tweets - int: a full list of tweets with all information regarding likes, user, retweets, etc.
def print_all_tweets(list_of_tweets):

    global positiveCount
    global negativeCount
    global neutralCount
    for tweet in list_of_tweets:
        tweet_value = find_tweet_value(list_of_tweets, tweet) #finding tweet value
        acc_value = find_account_value(tweet) #finding account value
        magnitude = getMagnitude(list_of_tweets, tweet)
        print(f"Verified: {tweet.user.verified}")
        print(f"{tweet.user.screen_name} tweeted: ") #prints username
        print("-----")
        print(tweet.text) #prints actual tweet text
        print("-----")
        print(f"# of likes: {tweet.favorite_count}") #prints likes
        likesArray.append(magnitude)
        print("----------------------------------------------------------------")
        print(f"# of likesArray: {likesArray}") #print all data
        print(f'# of retweets: {tweet.retweet_count}') #prints retweets
        print(f"Tweet Value: {tweet_value}") #prints tweet value
        print(f"Account Value: {acc_value}") #prints account value
        print(f"Tweet Magnitude: {magnitude}")

        #getting sentiment
        pol = getPolarity(tweet.text)
        sen = getSentiment(pol)
        if sen == "Positive":
        	positiveCount= positiveCount+1
        elif sen == "Negative":
        	negativeCount= negativeCount+1
        else:
        	neutralCount= neutralCount+1
        	
        print(f"Sentiment: {sen}") #prints sentiment
        

        print("-------------------------------------------------------------------------------")



#main function
def main():
    # user input
   
    user_search = input("What coin are you looking for? ")
    search_term = user_search + " -filter:retweets"

    # making a list of all tweets with my query
    search_tweets = api.search_tweets(q = search_term, lang = "en", count = 100000, result_type = "mixed")


    # shows me how many tweets api.search_tweets() gets
    print(user_search.upper())
    print(f"Number of tweets found: {len(search_tweets)}")
    print("------------------------------------------------------------------------------------------------------------------------")

    # loops through each tweet in search_tweets and prints information about each tweet
    print_all_tweets(search_tweets)
    
    connotation = getConnotation(search_tweets)
    print(f"CURRENT CONNOTATION: {connotation}")
    fig = plt.figure(figsize =(5, 3))
    plotArray = [positiveCount, negativeCount, neutralCount]
    plt.pie(plotArray,labels = sentiment)
    plt.show()

main()

