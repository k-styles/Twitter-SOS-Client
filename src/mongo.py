import logging
from pymongo import MongoClient

# Setup the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('mongo.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Not adding stream handler. Output logs to mongo.log file
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)


from .config import MONGO_URI

client = MongoClient(MONGO_URI)
logger.info('Starting Atlas client')

db = client.twitter_test_db
tweets = db.tweets

def insert_tweet(tweet):
	try:
		tweet_id = tweets.insert_one(tweet).inserted_id
	except Exception as e:
		logging.exception('Error inserting tweet')
	else:
		logger.debug('Added:tweet_id:'+str(tweet_id))