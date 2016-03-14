import json


def get_config():
    with open("config.json", 'r') as file:
        s = file.read()
        return json.loads(s)
