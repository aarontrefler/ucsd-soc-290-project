def print_tweet(tweet):
    """
    Print text for a tweet
    """
    print(tweet['text'])


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