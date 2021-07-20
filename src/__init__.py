import os
import json

file_path = ''
file_template = {
    "BEARER_TOKEN": None,
    "API_KEY": None,
    "API_SECRET_KEY": None,
    "ACCESS_TOKEN": None,
    "ACCESS_TOKEN_SECRET": None
}

try:
    with open(file_path, 'r') as file:
        creds_json = json.load(file)
        for key in creds_json.keys():
            os.environ[key] = creds_json[key]

except FileNotFoundError as fnf:
    with open(file_path, 'w') as file:
        json.dump(file_template, file, indent=4)