""" Argument parser for command line arguments."""

from .twitter_client import TwitterStreamingClient
from .config import BEARER_TOKEN, API_SECRET_KEY
from .utilities import get_rule_from_input

streamingClient = TwitterStreamingClient(BEARER_TOKEN, API_SECRET_KEY)

def parse_arguments(args):
	if(args.start):
		streamingClient.stream_tweets()
	if(args.getrules):
		rules = streamingClient.get_rules()
		return
	if(args.del_all_rules):
		streamingClient.delete_all_rules()
	if (args.del_id):
		ids_list = list(args.del_id.split(" "))
		streamingClient.delete_rules_by_ids(ids_list)
	if (args.del_val):
		values_list = list(args.del_val.split(","))
		for i in range(0,len(values_list)):
			values_list[i] = values_list[i].strip()
		streamingClient.delete_rules_by_values(values_list)
	if(args.add_rule):
		temp = get_rule_from_input()
		streamingClient.add_rules(temp)