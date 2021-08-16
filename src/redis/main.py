import argparse
from redis_client import parse_arguments
parser = argparse.ArgumentParser()

parser.add_argument('--get', 
                    action = 'store_true',
                    help = "Gets all the tweets")

parser.add_argument('--store',
                    action = 'store_true',
                    help = "Get and store the tweets in json file")

parser.add_argument('--flush',
                    action = "store_true",
                    help = "Delete the database")

ARGS = parser.parse_args()
parse_arguments(ARGS)