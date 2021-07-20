import json
import os

cwd = os.getcwd()

config_file_path = os.path.realpath(__file__)

config_file_path = config_file_path.replace(cwd, '')
creds_file_path_from_cwd = config_file_path.replace('config.py', 'credentials.json')[1:]

f = open(creds_file_path_from_cwd, 'r')

credentials_dict = json.load(f)