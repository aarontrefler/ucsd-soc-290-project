"""Code to create scores for Trump tweets in Mongodb."""
import pandas as pd
import re

from pymongo import MongoClient
from textblob import TextBlob


def clean_tweet(tweet):
    """Utility function to clean tweet text by removing links, special characters using simple regex statements."""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet['text']).split())


def get_tweet_sentiment(tweet):
    """Utility function to classify sentiment of passed tweet using textblob's sentiment method."""
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment.polarity


def build_scores(verbose=1):
    """TDB."""
    db = MongoClient().twitterdb

    scores = []
    for tweet in db.trump_tweets.find():
        if verbose > 0:
            print("\tScoring tweet {}".format(tweet['id_str']))
        scores.append({
            'id_str': tweet['id_str'],
            'score': get_tweet_sentiment(tweet),
            'text': tweet['text']
        })

    pd.DataFrame(scores).sort_values(by='score').to_csv("../../data/clean/scores.csv")

if __name__ == '__main__':
    print('Scoring tweets ...')
    build_scores()
