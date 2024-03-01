import yaml
import redis
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

class Assignment3:
    """_summary_
    """
    def __init__(self):
        """Initializes the class.

    Loads the configuration, establishes a Redis connection, sets API details,
    initializes json_response and df attributes.

    Args:
        self: The instance of the class.

    Returns:
        None
        """
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
        """Create a Redis connection using the config.yaml"""
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
        self.data_index = api_config['index']

    def read_api(self):
        """Execute API call and store in variable"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        # print(response.json())
        if response.status_code == 200:
            self.json_response = response.json()
        else:
            print(f"Error: {response.status_code}")

    def json_into_redis(self):
        """Load JSON response into Redis database"""
        if self.json_response:
            self.r.flushall()
            self.r.json().set(self.data_index, Path.root_path(), self.json_response)
            # self.r.json().set(self.data_index, '$', self.json_response)

    def read_data_from_redis(self):
        """Retrieve data from Redis and convert to DataFrame"""
        result = self.r.json().get(self.data_index)
        redis_JSON_output = self.r.json().get(self.data_index)['quoteSummary']['result'][0]['secFilings']['filings'][0]
        # print(redis_JSON_output)
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
        """Plot 'SEC Filings by Type' diagram and display"""
        if self.df is not None:
            fig, ax = plt.subplots()
            self.df['type'].value_counts().sort_values().plot(ax=ax, kind='barh')
            plt.suptitle('SEC Filings for "AMRN" by Type from 01-24-2022 to 02-12-2024')
            plt.show()
    
    def simple_search(self):
        """
        attempting a simple search, however not working yet.
        The following 2 lines are not functioning properly together
        I think the problem is in line 106 between 'filings' and 'type'       ↓
        """
        self.schema = TagField("$.quoteSummary.result.[0].secFilings.filings.[*].type", as_name="type")
        self.r.ft().create_index(self.schema, definition=IndexDefinition(prefix=["type:"], index_type=IndexType.JSON))
                 
        print(self.r.ft().search('PRE 14A'))
        # self.schema = TextField("$.user.name", as_name="name"),TagField("$.user.city", as_name="city"), NumericField("$.user.age", as_name="age")
        # result = self.r.json().get(self.data_index)
        # print(self.r.json().get(self.data_index)['quoteSummary']['result'][0]['secFilings']['filings'][0]['type'])