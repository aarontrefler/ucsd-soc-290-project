"""Transform Twitter data in local MongoDB into a raw dataset of csv files."""
import numpy as np
import pandas as pd

from pymongo import MongoClient


def create_raw_data(db, retweet_collections):
    """Extract retweet features for all collected Trump tweets."""
    # Get number of collections in database
    num_collections = len(retweet_collections)

    # Extract retweet features for all collected Trump tweets
    num_documents = []
    for count, collection in enumerate(retweet_collections):
        # Get number of documents in collection
        num_documents_retweet = db[retweet_collections[count]].count()
        num_documents.append(num_documents_retweet)

        print("Processing {retweets} retweets in collection {idx} of {num_collections}...".format(
            retweets=num_documents_retweet, idx=count + 1, num_collections=num_collections))

        # Extract retweet features for Trump tweet
        feats_retweets = []
        for _, retweet in enumerate(db[collection].find()):
            feats = {
                'trump_tweet_id': retweet['retweeted_status']['id_str'],
                'favorite_count': retweet['favorite_count'],
                'lang': retweet['lang'],
                'source': retweet['source'],
                'geo': retweet['geo'],
                'coordinates': retweet['coordinates'],
                'place': retweet['place'],
                'user_created_at': retweet['user']['created_at'],
                'user_description': retweet['user']['description'],
                'user_favourites_count': retweet['user']['favourites_count'],
                'user_followers_count': retweet['user']['followers_count'],
                'user_friends_count': retweet['user']['friends_count'],
                'user_lang': retweet['user']['lang'],
                'user_location': retweet['user']['location'],
                'user_name': retweet['user']['name'],
                'user_statuses_count': retweet['user']['statuses_count']
            }
            feats_retweets.append(feats)

    # Display summary statistics
    print("Total number of documents: {}".format(np.sum(num_documents)))
    print("Average number of documents per collection: {}".format(np.mean(num_documents)))
    print("Median number of documents per collection: {}".format(np.median(num_documents)))
    print("Minimum number of documents in a collection: {}".format(np.min(num_documents)))
    print("Maximum number of documents in a collection: {}".format(np.max(num_documents)))

    return pd.DataFrame(feats_retweets)


def transform_data():
    """Extract relevant Twitter data from database and save as csv files in raw data directory."""
    client = MongoClient()
    db = client.twitterdb

    # Get retweet collections
    retweet_collections = db.collection_names(include_system_collections=False)
    retweet_collections.remove('trump_tweets')

    # Extract retweet features for all collected Trump tweets
    df = create_raw_data(db, retweet_collections)

    # Save data as csv
    csv_dir = "../../data/interim/"
    csv_filename = str(df.trump_tweet_id[0]) + "_retweet_feats.csv"
    df.to_csv(csv_dir + csv_filename)


if __name__ == '__main__':
    transform_data()
