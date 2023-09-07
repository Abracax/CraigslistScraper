import json
import requests
import string

BASE_URL = "https://craigslist.org/suggest?type=makemodel"

def write_to_file(strings, filename):
    with open(filename, 'a') as f:
        for item in strings:
            f.write(f"{item}\n")

def construct_terms():
    letters = string.ascii_lowercase  # Get all lowercase letters (a-z)
    combinations = [a + b for a in letters for b in letters]
    return combinations
    
num_of_terms = 2000
terms = construct_terms()
res = set()
while True:
    next_term = []
    for term in terms:
        next_term = []
        new_params = {"term" : term}  # Adding/Updating the 'term' parameter
        response = requests.get(BASE_URL, params=new_params)

        if response.status_code == 200:
            print(f"Success for term {term}: {response.json()}")  # Assuming the response is in JSON format
            list_of_strings = response.json()
            list_of_strings = [_ for _ in list_of_strings if len(_) > 3 and _ != 'all' and _ != 'all all' and _ != 'any']
            if len(list_of_strings) > 10:
                list_of_strings = list_of_strings[:10]
            next_term.append(list_of_strings)
            for l in list_of_strings:
                res.add(l)

            num_of_terms -= len(list_of_strings)
            if (num_of_terms < 0):
                break
        else:
            print(f"Failed for term {term}: {response.status_code}")
    write_to_file(list(res), f'response_strings.txt')
    terms = next_term

