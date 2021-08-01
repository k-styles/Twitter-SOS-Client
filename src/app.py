""" Argument parser for command line arguments."""

from .twitter_client import TwitterStreamingClient
from .config import BEARER_TOKEN, API_SECRET_KEY

streamingClient = TwitterStreamingClient(BEARER_TOKEN, API_SECRET_KEY)

def parse_arguments(args):
	if(args.start):
		streamingClient.stream_tweets()
	if(args.getrules):
		rules = streamingClient.get_rules()
		print(rules)
	if(args.del_all_rules):
		streamingClient.delete_all_rules()
	if(args.stream_all_tweets):
		streamingClient.stream_tweets()