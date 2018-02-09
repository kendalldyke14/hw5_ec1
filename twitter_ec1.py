from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Tuesday 5:30-7
## Any names of people you worked with on this assignment: Kelsey Toporski, Natalie Cieslak

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username1 = sys.argv[1]
username2=sys.argv[2]
num_tweets = sys.argv[3]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Getting Tweets:
baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
params1 = {'screen_name': username1, "count": num_tweets}
params2 = {"screen_name": username2, "count": num_tweets }
auth = OAuth1(consumer_key,consumer_secret, access_token, access_secret)
response1 = requests.get(baseurl, params1, auth=auth)
response2 = requests.get(baseurl, params2, auth=auth)
tweet_data1 = json.loads(response1.text)
tweet_data2 = json.loads(response2.text)

#Code for Analyzing Tweets:
def analyze_tweets(tweet_data1, tweet_data2):
    tweet_content1 = " ".join([x["text"] for x in tweet_data1])
    tweet_content2 = " ".join([x['text'] for x in tweet_data2])
    tweet_content_both= tweet_content1 + " " + tweet_content2

    tokens_both = nltk.word_tokenize(tweet_content_both)
    freqDist_both = nltk.FreqDist(token for token in tokens_both if (token.isalpha() and ("RT" not in token) and ("http" not in token) and ("https" not in token)))

    tokens1 = nltk.word_tokenize(tweet_content1)
    tokens2 = nltk.word_tokenize(tweet_content2)
    freqDist1 = nltk.FreqDist(token for token in tokens1 if (token.isalpha() and ("RT" not in token) and ("http" not in token) and ("https" not in token) and (token not in tokens2)))
    freqDist2 = nltk.FreqDist(token for token in tokens2 if (token.isalpha() and ("RT" not in token) and ("http" not in token) and ("https" not in token) and (token not in tokens1)))
    return [freqDist_both.most_common(5), freqDist1.most_common(5), freqDist2.most_common(5)]

analyze_tweets(tweet_data1, tweet_data2)

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
    else:
        print("USERS: {} and {}".format(username1, username2))
        print("TWEETS ANALYZED: {}".format(num_tweets))
        print("5 MOST FREQUENT COMMON WORDS IN BOTH {} and {}: ".format(username1, username2) + " ".join([(word + "(" + str(frequency) + ")") for word, frequency in analyze_tweets(tweet_data1, tweet_data2)[0]]))
        print("5 MOST FREQUENT (UNIQUE) WORDS IN " + username1 + ": " + " ".join([(word + "(" + str(frequency) + ")") for word, frequency in analyze_tweets(tweet_data1, tweet_data2)[1]]))
        print("5 MOST FREQUENT (UNIQUE) WORDS IN " + username2 + ": " + " ".join([(word + "(" + str(frequency) + ")") for word, frequency in analyze_tweets(tweet_data1, tweet_data2)[2]]))
