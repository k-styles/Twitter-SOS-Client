#!/usr/bin/env python3

import argparse
import json

import src
from src.app  import parse_arguments

version = "0.10."

parser = argparse.ArgumentParser()


parser.add_argument("-st",
					"--start",
					help="Start the application",
					action="store_true")

parser.add_argument("-gr",
					"--getrules",
					help="Get the current rules",
					action="store_true")


ARGV = parser.parse_args()
# print(ARGV)
parse_arguments(ARGV)

# Define credentials dictionary
# cred_dict = {
#     'BEARER_TOKEN': ARGV.bearer_token,
#     'API_KEY': ARGV.api_key,
#     'API_SECRET_KEY': ARGV.api_secret_key,
#     'ACCESS_TOKEN': ARGV.access_token,
#     'ACCESS_TOKEN_SECRET': ARGV.access_token_secret
# }

# Create json object from credentials dictionary
# cred_json = json.dumps(cred_dict, indent = 4)

# Open and write the credentials json object in /src'credentials.json' file
""" with open('src/credentials.json', 'a') as f:
    if()
		f.write(cred_json)

parse_arguments(ARGV) """