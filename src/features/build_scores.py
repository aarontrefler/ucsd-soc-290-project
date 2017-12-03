"""Code to create scores for Trump tweets in Mongodb."""
import pandas as pd
import re

from pymongo import MongoClient
from sklearn.preprocessing import MinMaxScaler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def normalize_scores(df, scores):
    """TDB."""
    for score in scores:
        scalar = MinMaxScaler(feature_range=(0, 1))
        df[score] = scalar.fit_transform(df[score].values.reshape(-1, 1))
    return df


def add_scores_emotion(df):
    """
    Add emotion scores.

    This is not called by train_model. Must be run seperately if desired.

    Emotion scores only available for first 256 tweets collected.

    Work done by Shaida on 11/28/17
    """
    df_scores_emotion = pd.read_csv("../../data/clean/scores_emotion.csv").drop(['anticipation', 'disgust', 'fear',
                                                                                 'joy', 'positive', 'sadness',
                                                                                 'surprise', 'trust'], axis=1)
    df = df.merge(right=df_scores_emotion, how='inner', on='id_str').drop(['Unnamed: 0'], axis=1)
    df = normalize_scores(df=df, scores=['anger', 'negative'])
    df['score'] = (df['anger'] + df['negative'] + (2 * df['score_keyword']) + df['score_textblob_pattern_sentiment'] +
                  df['score_textblob_bayes_sentiment']) / 6
    df.sort_values('score', ascending=False).to_csv("../../data/clean/scores_combined.csv")


def clean_tweet(tweet):
    """Utility function to clean tweet text by removing links, special characters using simple regex statements."""
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet['text']).split())


def textblob_bayes_sentiment(tweet):
    """
    Utility function to classify sexntiment of passed tweet.

    Using textblob's sentiment method using the PatternAnalyzer.
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    return ((analysis.sentiment.polarity * -1) + 1) / 2


def textblob_pattern_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet.

    Using textblob's sentiment method using the NaiveBayesAnalyzer.
    """
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet), analyzer=NaiveBayesAnalyzer())
    return analysis.sentiment.p_neg


def keyword_score(tweet):
    """TDB."""
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
            'text': tweet['text'],
            'score_keyword': keyword_score(tweet),
            'score_textblob_pattern_sentiment': textblob_pattern_sentiment(tweet),
            'score_textblob_bayes_sentiment': textblob_bayes_sentiment(tweet)
        })
    df_scores = normalize_scores(df=pd.DataFrame(scores), scores=['score_keyword', 'score_textblob_pattern_sentiment',
                                                                  'score_textblob_bayes_sentiment'])
    df_scores['score'] = (df_scores[['score_keyword', 'score_textblob_pattern_sentiment',
                                     'score_textblob_bayes_sentiment']].mean(axis=1))
    df_scores.sort_values('score', ascending=False).to_csv("../../data/clean/scores.csv")
    return df_scores


if __name__ == '__main__':
    #print('Scoring tweets ...')
    #df_scores = build_scores()

    #TEMP
    df_scores = pd.read_csv("../../data/clean/scores.csv").drop("Unnamed: 0", axis=1)
    
    print('Combine with emotion scores ...')
    add_scores_emotion(df_scores)
