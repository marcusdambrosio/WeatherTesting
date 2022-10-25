from urllib.request import urlopen
from pandas.io.json import json_normalize
import json
import pandas as pd

api_key = ""
date = "20170714"
zip_code = "92277"

response = urlopen("http://api.wunderground.com/api/%s/history_%s/q/%s.json" % (api_key, date, zip_code))

json_data = response.read().decode('utf-8', 'replace')

data = json.loads(json_data)

for observation in data['history']['observations']:
    print("Date/Time: " + observation['date']['pretty'])
    print("Temperature: " + observation['tempi'])
    print("Humidity: " + observation['hum'])

df = json_normalize(data['history']['observations'])

df = df[['date.pretty', 'tempi', 'hum']]
df['date.pretty'] = pd.to_datetime(df['date.pretty'])

print(df)
sys.exit()
# Create CSV
df.to_csv('C:\WeatherUnderGround\Test.csv')

# Append CSV
# df.to_csv('C:\WeatherUnderGround\Test.csv', na_rep='-99999', columns=None, header=False, index=True, index_label=None, mode='a')