import requests
import json
import utils

config = utils.load_config()

url = config['API']['JSON_placeholder']['url']

response = requests.get(url)

# url = config['API']['Crime']['url']
# params = config['API']['Crime']['params']
# headers = config['API']['Crime']['headers']
# response = requests.get(url, params)

if response.status_code == 200:
    response = response.json()
    print(type(response))
    #print(response)
    JSON_response = response
    print('JSON converson below:')
    print(type(JSON_response))
    #print(JSON_response)
else:
    print(f"Error: {response.status_code}")