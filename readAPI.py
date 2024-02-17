import requests
import json
import utils

# config = utils.load_config()
# url = config['API']['JSON_placeholder']['url']
# response = requests.get(url)

# url = config['API']['Crime']['url']
# params = config['API']['Crime']['params']
# headers = config['API']['Crime']['headers']
# response = requests.get(url, params)

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-sec-filings"

querystring = {"symbol":"AMRN","region":"US","lang":"en-US"}

headers = {
	"X-RapidAPI-Key": "a0dd196a09mshcacea72b440d8e9p15578ajsnb703b6903e99",
	"X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    JSON_response = response.json()
    #print(type(response))
    #print(response)
    #JSON_response = response
    #print('JSON converson below:')
    #print(type(JSON_response))
    #print(JSON_response)
else:
    print(f"Error: {response.status_code}")