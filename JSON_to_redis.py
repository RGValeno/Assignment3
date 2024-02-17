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
print(type(result))
#print(result)

df = pd.DataFrame(result)
print(df)
print(df.columns.tolist())