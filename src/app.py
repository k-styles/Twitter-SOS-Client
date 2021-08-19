""" Argument parser for command line arguments."""

import _thread

from pprint import pprint

from .twitter_client import TwitterStreamingClient
from .utilities import get_rule_from_input, scheduler
from .db import insert_cache_tweets_to_db
from .config import DELAY, BEARER_TOKEN, API_SECRET_KEY

streamingClient = TwitterStreamingClient(BEARER_TOKEN, API_SECRET_KEY)

def parse_arguments(args):
	if(args.start):
		_thread.start_new_thread(streamingClient.stream_tweets, ())
		_thread.start_new_thread(scheduler, (DELAY, insert_cache_tweets_to_db))
		while 1:
			pass
    
	if(args.getrules):
		rules = streamingClient.get_rules()
		pprint(rules, indent=4)
  
	if(args.del_all_rules):
		resp = streamingClient.delete_all_rules()
		pprint(resp, indent=4)

	if (args.del_id):
		ids_list = list(args.del_id.split(" "))
		resp = streamingClient.delete_rules_by_ids(ids_list)
		pprint(resp, indent=4)
    
	if (args.del_val):
		values_list = list(args.del_val.split(","))
		for i in range(0,len(values_list)):
			values_list[i] = values_list[i].strip()
		resp = streamingClient.delete_rules_by_values(values_list)
		pprint(resp, indent=4)
    
	if(args.add_rule):
		temp = get_rule_from_input()
		streamingClient.add_rules(temp)
