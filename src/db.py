import logging
from pymongo import MongoClient
import redis
import json

# Setup the logger
mongo_logger = logging.getLogger("mongo")
mongo_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("mongo.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
mongo_logger.addHandler(file_handler)

redis_logger = logging.getLogger("redis")
redis_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("redis.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
redis_logger.addHandler(file_handler)

from .config import MONGO_URI

client = MongoClient(MONGO_URI)
mongo_logger.info("Starting Atlas client")

# Connect to the Server
try:
    redis_logger.info("Connecting to redis server")
    r = redis.Redis()
except Exception as e:
    redis_logger.exception(e)

db = client.twitter_test_db
tweets = db.tweets


def insert_tweet(tweet):
    try:
        tweet_id = tweets.insert_one(tweet).inserted_id
    except Exception as e:
        mongo_logger.exception("Error inserting tweet:", e)
    else:
        mongo_logger.debug("Added:tweet_id:" + str(tweet_id))


def insert_bulk_tweets(tweets_list):
    # TODO: Add bulk adding function
    try:
        tweet_id = tweets.insert_many(tweets_list).inserted_ids
    except Exception as e:
        mongo_logger.exception("Error inserting tweets list:", e)
    else:
        mongo_logger.debug("Added:tweet_id:" + str(tweet_id))


def add_tweet_to_cache(tweet):
    try:
        r.lpush("tweets", json.dumps(tweet))
    except Exception as e:
        redis_logger.exception("Error adding tweet to cache:", e)
    else:
        redis_logger.debug("Added:tweet_id:" + str(tweet["data"]["id"]))


def fetch_tweets_and_clear_cache():
    tweets = list()
    try:
        while r.llen("tweets") != 0:
            tweets.append(json.loads(r.lpop("tweets").decode("utf-8")))
    except Exception as e:
        redis_logger.exception("Error popping tweets from caches:", e)
    else:
        return tweets


def insert_cache_tweets_to_db():
    tweets = fetch_tweets_and_clear_cache()
    if tweets:
        insert_bulk_tweets(tweets)
