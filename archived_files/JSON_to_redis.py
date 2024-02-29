"""takes api response and inputs it to redis db

Returns:
    json from redis db for verification
"""

import readAPI
import utils
import json
from redis.commands.json.path import Path
from db_config import get_redis_connection

import pandas as pd
import matplotlib.pyplot as plt

config  = utils.load_config()
r       = get_redis_connection()
data    = config['API']['JSON_placeholder']['index']


def JSON_into_REDIS():


##### Input JSON into redis
r.flushall()
r.json().set(data, '$', readAPI.JSON_response)


##### Get data from Redis
result = r.json().get(data)
df_list = result['quoteSummary']['result'][0]['secFilings']
df = pd.DataFrame(df_list['filings'])
df = df[['date', 'type', 'title', 'edgarUrl']]
#print(df)


##### Data Manipulation
df['date'] = df['date'].apply(pd.to_datetime)
df['type'] = pd.Categorical(df.type)
df['title'] = pd.Categorical(df.title)
df['edgarUrl'].astype(str)
#print(df.dtypes)


##### Plot diagram and display
fig, ax = plt.subplots()
df['type'].value_counts().plot(ax=ax, kind='barh')
plt.suptitle('SEC Filings by Type from 01-24-2022 to 02-12-2024')
plt.show(block=True)