import json
import tweepy
import os

from tweepy import OAuthHandler
from pymongo import MongoClient


def store_tweet(tweet, collection):
    """
    Store tweet in MongoDB
    """
    db[collection].insert_one(tweet)


def limit_handled(cursor):
    """
    Code taken from tweepy to deal with rate limit issues
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("Rate limit exceeded. Sleeping ...")
            time.sleep(15 * 60)


def get_trump_tweets(n):
	"""
	Get Trump tweets from his Twitter timeline
	"""
	for tweet in limit_handled(tweepy.Cursor(
    	api.user_timeline, id='realDonaldTrump', count=n).items(n)):
    	#store_tweet(tweet=tweet._json, collection='trump_tweets')


def setup_api(keys):
	"""
	Setup tweepy API object
	"""
	auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
	auth.set_access_token([keys['access_token'], keys['access_secret'])
	api = tweepy.API(auth)
	return api


def get_keys():
	"""
	Get Twiiter API keys
	"""
	keys = {}
	keys['consumer_key'] = 'W1vEEpGJawjrqeW70yBUkfrWt'
	keys['consumer_secret'] = 'PSNivPYzJCjvEeQ5WW0zAhAIbAoEdzQBjTUG39up4yhnW9HABi'
	keys['access_token'] = '289683843-a9GiDa84Ak7FqD8c8Cu1qYzA5oEVqQ1FSKjkSudP'
	keys['access_secret'] = 'O3KhEusOxqTJGI6zvh8eqlDbyGyUT4tKThymbr57YFHWx'
	return keys


def extract_data():
	"""
	"""
	# Twitter API setup
	keys = get_keys()
	api = setup_api(keys)
	user = api.get_user('realDonaldTrump')

	# MongoDB setup
	#os.system('mongo twitterdb --eval "db.dropDatabase();"')
	client = MongoClient()
	db = client.twitterdb

	# Get Trump tweets
	get_trump_tweets(n=1)

	# Get Trump retweets
	#get_trump_retweets(n=100)

	
if __name__ == '__main__':
	extract_data()
