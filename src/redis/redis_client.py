import redis
from . import redis_login
import json

# Connect to the Server
r = redis.Redis(
    host = redis_login.HOSTNAME,
    port = redis_login.PORT,
    password = redis_login.PASSWORD
)

def parse_arguments(args):
    # Gets tweets from database and stores them in file redis_tweets.json
    if(args.get and not bool(args.store)):
        byte_tweets = r.execute_command('JSON.GET object')
        try:
            string_tweets = byte_tweets.decode('utf-8')
        except AttributeError:
            raise Exception('Empty Database!')

        """ string_tweets_r_prefixed = string_tweets.encode('unicode_escape').decode() """

        json_tweets = json.loads(string_tweets)

        with open('redis_tweets.json', 'w') as f:
            json.dump(json_tweets, f, indent=4)

    # Stores tweets in database from streamed_tweet.json
    if(args.store and not bool(args.get)):
        # Open tweets file and store it as a dictionary in a variable
        file = open('streamed_tweets.json')
        tweets_json = json.load(file)

        # Set variable object as the json object in Redis Server
        r.execute_command('JSON.SET', 'object', '.', json.dumps(tweets_json))
    
    # Clears up the database
    if(args.flush):
        r.execute_command('FLUSHDB')

def insert_tweet(tweet):
    tweets_json = json.dumps(tweet, indent=4)
    try:
        r.execute_command('JSON.SET', 'object', '.', json.dumps(tweets_json))
    except Exception as error:
        print("Error inserting tweet in cache")