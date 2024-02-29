import yaml
import redis
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from redis.commands.json.path import Path


class assignment_3:
    
    #config      = load_config()
    #r           = get_redis_connection()
    
    #url         = config['API']['SEC_filings']['url']
    #headers     = config['API']['SEC_filings']['headers']
    #params      = config['API']['SEC_filings']['querystring']
    #data        = config['API']['JSON_placeholder']['index']
    #response    = requests.get(url, headers=headers, params=params)
    
    
    def __init__(self, config, url, headers, params, data, response, r):
        self.config = self.load_config()
        self.r = self.get_redis_connection()
        self.config = config
        self.url = url
        self.headers = headers
        self.paraps = params
        self.data = data
        self.response = response
    
    
    def load_config():
        """ - Load configuration from the YAML file.

        Returns:
            dict: Configuration data.
        """
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    

    def get_redis_connection():
        """ - Create a Redis connection using the configuration.

        Returns:
            Redis: Redis connection object.
        """
        return redis.Redis(
            host=config["redis"]["host"],
            port=config["redis"]["port"],
            db=0,
            decode_responses=True,
            username=config["redis"]["user"],
            password=config["redis"]["password"],
        )


    def read_api():
        """ - execute api call and store in variable
        """
        url         = config['API']['SEC_filings']['url']
        headers     = config['API']['SEC_filings']['headers']
        params      = config['API']['SEC_filings']['querystring']
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            JSON_response = response.json()
        else:
            print(f"Error: {response.status_code}")
        
        
    def JSON_into_REDIS():
        """ - load JSON into redis db
        """
        data        = config['API']['JSON_placeholder']['index']
        
        r.flushall()
        r.json().set(data, '$', readAPI.JSON_response)
        
        
    def read_data_from_redis():
        """ - get the data from redis
            - convert from JSON to dataframe using pandas
            - rename the columns
        """
        result = r.json().get(data)
        df_list = result['quoteSummary']['result'][0]['secFilings']
        df = pd.DataFrame(df_list['filings'])
        df = df[['date', 'type', 'title', 'edgarUrl']]
        #print(df)
        
        
    def clean_data():
        """ - clean and manipulte data
        """
        df['date'] = df['date'].apply(pd.to_datetime)
        df['type'] = pd.Categorical(df.type)
        df['title'] = pd.Categorical(df.title)
        df['edgarUrl'].astype(str)
        #print(df.dtypes)
        
        
    def plot_diagram():
        """ - plot diagram and display
        """
        fig, ax = plt.subplots()
        df['type'].value_counts().plot(ax=ax, kind='barh')
        plt.suptitle('SEC Filings by Type from 01-24-2022 to 02-12-2024')
        plt.show(block=True)