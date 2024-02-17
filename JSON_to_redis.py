import readAPI
import utils
import json
from redis.commands.json.path import Path
from db_config import get_redis_connection

import pandas as pd

config = utils.load_config()
r = get_redis_connection()
r.flushall()
data = config['API']['JSON_placeholder']['index']

r.json().set(data, '$', readAPI.JSON_response)

result = r.json().get(data)
print('**********************reading from redis**********************')

df_list = result['quoteSummary']['result'][0]['secFilings']
df = pd.DataFrame(df_list['filings'])
print(list(df.columns.values))
df = df[['date', 'type', 'title', 'edgarUrl']]
print(df)
df['date'] = df['date'].apply(pd.to_datetime)
df['type'] = pd.Categorical(df.type)
df['title'] = pd.Categorical(df.title)
df['edgarUrl'].astype(str)
print(df.dtypes)