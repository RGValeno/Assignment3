import yaml
import redis
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from redis.commands.json.path import Path

class Assignment3:

    def __init__(self):
        self.config = self.load_config()  # Load configuration at initialization
        self.r = self.get_redis_connection()  # Establish Redis connection
        self.set_api_details()  # Set API details from the loaded configuration
        self.json_response = None  # Initialize json_response to None
        self.df = None  # Initialize DataFrame to None

    @staticmethod
    def load_config():
        """Load configuration using config.yaml"""
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)

    def get_redis_connection(self):
        """Create a Redis connection using the config.yaml."""
        return redis.Redis(
            host=self.config["redis"]["host"],
            port=self.config["redis"]["port"],
            db=0,
            decode_responses=True,
            username=self.config["redis"]["user"],
            password=self.config["redis"]["password"],
        )

    def set_api_details(self):
        """Set API details using config.yaml"""
        api_config = self.config['API']['SEC_filings']
        self.url = api_config['url']
        self.headers = api_config['headers']
        self.params = api_config['querystring']
        self.data_index = self.config['API']['JSON_placeholder']['index']

    def read_api(self):
        """Execute API call and store in variable."""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            self.json_response = response.json()
        else:
            print(f"Error: {response.status_code}")

    def json_into_redis(self):
        """Load JSON response into Redis database."""
        if self.json_response:
            self.r.flushall()
            self.r.json().set(self.data_index, Path.root_path(), self.json_response)

    def read_data_from_redis(self):
        """Retrieve data from Redis and convert to DataFrame."""
        result = self.r.json().get(self.data_index)
        if result:
            df_list = result['quoteSummary']['result'][0]['secFilings']['filings']
            self.df = pd.DataFrame(df_list)

    def clean_data(self):
        """Create new dataframe with subset of columns and change datatypes"""
        if self.df is not None:
            self.df = self.df[['date', 'type', 'title', 'edgarUrl']]
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df['type'] = pd.Categorical(self.df['type'])
            self.df['title'] = pd.Categorical(self.df['title'])
            self.df['edgarUrl'] = self.df['edgarUrl'].astype(str)

    def plot_diagram(self):
        """Plot diagram and display."""
        if self.df is not None:
            fig, ax = plt.subplots()
            self.df['type'].value_counts().sort_values().plot(ax=ax, kind='barh')
            plt.suptitle('SEC Filings by Type from 01-24-2022 to 02-12-2024')
            plt.show()