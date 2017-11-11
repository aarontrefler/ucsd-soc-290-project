"""
Load MongoDB with Twitter data
"""
import json
import os
import os.path
import pprint
from pymongo import MongoClient


def test_load():
    """
    Test MongoDB loaded correctly
    """
    client = MongoClient()
    db = client.twitterdb
    
    print("Extracting Trump tweet ...")
    pprint.pprint(db.trump_tweets.find_one())
    print("Number of collections: {}".format(len(db.collection_names())))


def load_data():
    """
    """
    # Assert currently in correct dir
    assert(os.path.isdir("../../data/twitterdb")), "../../data/twitterdb does not exist"

    # Restore MongoDB
    os.system('mongorestore --drop --db twitterdb --gzip --dir ../../data/twitterdb')

    # Test resotre
    test_load()


if __name__ == '__main__':
    load_data()