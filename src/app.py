""" Argument parser for command line arguments.
"""
from twitter_client import TwitterStreamingClient
from config import credentials_dict

streamingClient = TwitterStreamingClient(credentials_dict['BEARER_TOKEN'], credentials_dict['API_SECRET_KEY'])

def parse_arguments(args):
	if(args.start):
		# TODO: Implement starting the app
		pass
	if(args.getrules):
		# TODO: Implement starting the app
		rules = streamingClient.get_rules()
		print(rules)