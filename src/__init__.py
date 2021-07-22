import os
import json
from pathlib import Path

file_path = str(Path(os.getcwd()).joinpath('src').joinpath('credentials.json'))

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
            if(creds_json[key]):
                os.environ[key] = creds_json[key]

except FileNotFoundError as fnf:
    with open(file_path, 'w') as file:
        json.dump(file_template, file, indent=4)