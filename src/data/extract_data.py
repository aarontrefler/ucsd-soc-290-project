"""
Extract new Trump tweet and retweet data from Twitter
"""
import json
import tweepy
import os
import sys

from tweepy import OAuthHandler
from pymongo import MongoClient


def store_tweet(tweet, db, collection):
    """
    """
    db[collection].insert_one(tweet._json)


def get_retweets(api, tweet, n):
    """
    """
    return api.retweets(tweet._json['id_str'], count=n)


def check_tweet_stored(tweet, db, collection):
    """
    Returns True if the database collection contains the tweet
    """
    if db[collection].find_one({'id_str': tweet._json['id_str']}) is not None:
        return True
    else:
        return False


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


def get_trump_tweets(n, api, db):
    """
    Get Trump tweets from his Twitter timeline
    """
    for counter, tweet in enumerate(limit_handled(
        tweepy.Cursor(api.user_timeline, id='realDonaldTrump', count=1).items(n))):
        # Check if tweet is already stored in twitterdb
        if check_tweet_stored(tweet=tweet, db=db, collection='trump_tweets'):
            print("Tweet {} already containted in db".format(counter))
            continue
        # Store tweet
        print("Storing tweet {}...".format(counter))
        store_tweet(tweet=tweet, db=db, collection='trump_tweets')
        # Store retweets
        print("Storing tweet {} retweets...".format(counter))

        for retweet in get_retweets(api=api, tweet=tweet, n=300):
            store_tweet(tweet=retweet, db=db, collection="trump_retweets_" + str(tweet._json['_id']))


def setup_api(keys):
    """
    Setup tweepy API object
    """
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

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


def extract_data(n):
    """
    """
    # Twitter API setup
    keys = get_keys()
    api = setup_api(keys)
    user = api.get_user('realDonaldTrump')

    # MongoDB setup
    client = MongoClient()
    db = client.twitterdb

    # Get Trump tweets and retweets
    get_trump_tweets(n=n, api=api, db=db)

    # Export MongoDB
    os.system('mongodump --db twitterdb --gzip --out "../../data"')


if __name__ == '__main__':
    # Set how many trump tweets to process
    if sys.argv[1]:
        n = int(sys.argv[1])
    else:
        n = 100

    extract_data(n=n)
