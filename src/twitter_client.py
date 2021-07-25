""" Twitter API v2 Streaming Client

Functionalities provided are:
1. Add rules
2. Fetch rules
3. Delete rules by value
4. Delete rules by id
5. Delete all rules
6. Stream tweets
"""
import requests
import os
import json
import warnings

from requests.models import StreamConsumedError


#---------Some Useful Functions---------#
# Extract and returns a list of valuesof the rules that already been set up
def extract_values(rules):
    return list(map(lambda rule: rule["value"], rules["data"]))

# Extract and returns a list of ids of the rules that already have been set up
def extract_ids(rules):
    return list(map(lambda rule: rule["id"], rules["data"]))

# This function stores all the streaming tweets to a JSON file.
def Tweets_to_JSON(streamed_tweets_filename, tweet):
    with open(streamed_tweets_filename, 'a') as tf:
        if(os.stat(streamed_tweets_filename).st_size>1):
            tf.write(',')
        elif(os.stat(streamed_tweets_filename).st_size==0):
            tf.write('[\n')

        tf.write(str(tweet))
        tf.write("\n")


class TwitterStreamingClient:

    def __init__(self, BEARER_TOKEN, API_SECRET_KEY):
        self.set_token = BEARER_TOKEN
        self.api_secret_key = API_SECRET_KEY

    # Provide rules and Bearer Token to add rules to the Twitter API
    def add_rules(self, rules):
        payload = {"add": [rules]}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)},
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        response_json = json.loads(response.text)

        # Check for duplicate rule error. Otherwise pass.
        try:
            if response_json['errors'][0]['title'] == 'DuplicateRule':
                warnings.warn("This rule has already been set up")
            else:
                pass
        except:
            print("Added Rules: ", payload)


        return json.dumps(response.json())

    # Provide Bearer Token to Retrieve Rules from the Twitter API
    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)}
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        print(json.dumps(response.json()))
        return response.json()

    # Deletes rules according to the Values provided as a list
    def delete_rules_by_values(self, values):

        #values = list(map(lambda rule: rule["values"], rules["data"]))
        payload = {"delete": {"values": values}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)},
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json())

    # Deletes rules according to the IDs provided as a list
    def delete_rules_by_ids(self, ids):

        #ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)},
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return json.dumps(response.json())

    # Provide Secret API Key to delete all the rules set up earlier
    def delete_all_rules(self):
        
        confirm = input("Please Confirm that you really want to DELETE all the Rules that you have set up earlier. Enter your API Secret Key: ")
        if confirm==self.api_secret_key:
            # First get all the rules
            rules = self.get_rules()

            # Now delete all the rules using ids (or values)
            if rules is None or "data" not in rules:
                return None

            ids = list(map(lambda rule: rule["id"], rules["data"]))
            payload = {"delete": {"ids": ids}}
            response = requests.post(
                "https://api.twitter.com/2/tweets/search/stream/rules",
                headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)},
                json=payload
            )
            if response.status_code != 200:
                if response.status_code == 403:
                    print("client-not-enrolled/Unauthorized")
                if response.status_code == 400:
                    print("One or more parameters to your request was invalid.")
                raise Exception(
                    "Cannot delete rules (HTTP {}): {}".format(
                        response.status_code, response.text
                    )
                )
            return json.dumps(response.json())

    # Opens up a stream of tweets by providing Bearer token
    def stream_tweets(self, store_to_json=False, streamed_tweets_filename=None):
        from .mongo import insert_tweet
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(self.set_token)},
            stream=True,
            params={"tweet.fields":"attachments,author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld",
                    "expansions":"referenced_tweets.id"
            }
        )

        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )

        for response_line in response.iter_lines():
            if response_line:
                if store_to_json:
                    json_response_python_dict = json.loads(response_line)
                    json_obj = json.dumps(json_response_python_dict, indent=4, sort_keys=True)
                    Tweets_to_JSON(streamed_tweets_filename, json_obj)

                json_response_python_dict = json.loads(response_line)
                # return json.dumps(json_response_python_dict, indent=4, sort_keys=True)
                insert_tweet(json_response_python_dict)

if __name__ == '__main__':
    #### SET YOUR RULES OVER HERE ####
    #rules_to_be_added = None

    # Add/set Rules
    #add_rules(BEARER_TOKEN, rules_to_be_added)

    # Retrieve Rules
    #rules = get_rules(BEARER_TOKEN)

    ## Delete Rules by IDs
    #ids = extract_ids(rules)    # Provides IDs of all rules
    #delete_rules_by_ids(BEARER_TOKEN, ids)


    ## Delete Rules by Values
    #values = extract_values(rules)  # Provides Values of all rules
    #delete_rules_by_values(BEARER_TOKEN, values)


    # Deletes all the rules that have been set up
    #delete_all_rules(BEARER_TOKEN)


    # Stream Tweets (try-except blocks completes the json file by adding ] at the end)
    store_to_json = True
    # Before setting store_to_json=True, Please Make sure your JSON file does not exist or is empty!
    if store_to_json:
        streamed_tweets_filename = 'streamed_tweets.json'
        try:
            # stream_tweets(BEARER_TOKEN, store_to_json=store_to_json, streamed_tweets_filename=streamed_tweets_filename)
            pass
        except KeyboardInterrupt:
            with open(streamed_tweets_filename, 'a') as tf:
                tf.write(']')

    else:
        streamed_tweets_filename = None
        # stream_tweets(BEARER_TOKEN, store_to_json=store_to_json, streamed_tweets_filename=streamed_tweets_filename)
