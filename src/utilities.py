import json

def get_rule_from_input():
    value = input("Enter the value:")
    tag = input("Enter the tag:")
    test_dict = {}
    test_dict["value"] = value
    test_dict["tag"] = tag
    return test_dict
