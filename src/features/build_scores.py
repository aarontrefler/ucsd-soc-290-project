"""Code to create scores for Trump tweets in Mongodb."""
import pandas as pd
import re

from pymongo import MongoClient
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def clean_tweet(tweet):
    """Utility function to clean tweet text by removing links, special characters using simple regex statements."""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet['text']).split())


def textblob_bayes_sentiment(tweet):
    """
    Utility function to classify sexntiment of passed tweet using textblob's sentiment method using the 
    PatternAnalyzer.
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    return ((analysis.sentiment.polarity * -1) + 1) / 2


def textblob_pattern_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet using textblob's sentiment method using the 
    NaiveBayesAnalyzer.
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer())
    return analysis.sentiment.p_neg


def keyword_score(tweet):
    keywords = ["hillary", "dem", "democrats", "email", "emails", "muslim", "muslim", "fake news", "mexican",
                "mexicans", "travel ban", "cnn"]
    score = 0
    for keyword in keywords:
        if keyword in clean_tweet(tweet).lower().split():
            score += 1
    return score / len(keywords)


def build_scores(verbose=1):
    """TDB."""
    db = MongoClient().twitterdb

    scores = []
    num_tweets = db.trump_tweets.count()
    for counter, tweet in enumerate(db.trump_tweets.find(no_cursor_timeout=True)):
        if verbose > 0:
            print("\tScoring tweet {id}: {i} of {tweets}".format(id=tweet['id_str'], i=counter,
                  tweets=num_tweets))
        scores.append({
            'id_str': tweet['id_str'],
            'score_keyword': keyword_score(tweet),
            'score_textblob_pattern_sentiment': textblob_pattern_sentiment(tweet),
            'score_textblob_bayes_sentiment': textblob_bayes_sentiment(tweet),
            'avg_score': (textblob_pattern_sentiment(tweet) + textblob_bayes_sentiment(tweet) + keyword_score(tweet))
                          / 3,
            'text': tweet['text']
        })
    pd.DataFrame(scores).sort_values(by='avg_score').to_csv("../../data/clean/scores.csv")

if __name__ == '__main__':
    print('Scoring tweets ...')
    build_scores()
