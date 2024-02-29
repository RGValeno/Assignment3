import requests
import json
import utils

config  = utils.load_config()
url     = config['API']['SEC_filings']['url']
headers = config['API']['SEC_filings']['headers']
params  = config['API']['SEC_filings']['querystring']


##### Execute API call
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    JSON_response = response.json()
else:
    print(f"Error: {response.status_code}")