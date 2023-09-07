import json
from .exceptions import InvalidJsonException

CITY_LIST = 'craigslistscraper/data/cities.csv'

def read_config(path):
        try:
            with open(path, 'r') as f:
                input_config = json.load(f)
        except FileNotFoundError:
            raise InvalidJsonException(path, "The provided config file path is incorrect.")
        except json.JSONDecodeError:
            raise InvalidJsonException(path, "The provided config file is not a valid JSON.")
        return input_config

def read_cities():
    with open(CITY_LIST, 'r') as f:
        cities = f.read().splitlines()
    return cities