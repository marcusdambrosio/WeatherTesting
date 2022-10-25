import requests
import pandas as pd
import datetime as dt
import os, sys, time
import numpy as np
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from pyowmap import owmAPIKEY, OwmWeather
import types

'''CONSTANTS'''
url = "https://visual-crossing-weather.p.rapidapi.com/history" #base URL for request
headers = {
    'x-rapidapi-key': "114cf1f22fmsh8560eeea8263157p1ea0e5jsnbb45041bee39",
    'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
}
unitGroup = 'us' #imperial units
contentType = 'csv' #pull data in csv format;;JSON also available
timezone = 'Z' #UTC time

class MasterWeather(OwmWeather):
    def __init__(self, lat, long, timestamp , cumulativeHrs = 1):
        super().__init__(timestamp, lat, long)
        self.lat = lat
        self.long = long
        self.reverse_geocode()
        self.startTS = timestamp - (60*60*24)
        self.endTS = timestamp
        self.start = dt.datetime.utcfromtimestamp(self.startTS).strftime('%Y-%m-%dT%H:%M:%S')
        self.end = dt.datetime.utcfromtimestamp(self.endTS).strftime('%Y-%m-%dT%H:%M:%S')
        self.latlong = str(lat)+','+str(long)
        self.querystring = {"startDateTime":self.start,
                           "aggregateHours":cumulativeHrs,
                           "location":self.latlong,
                           "endDateTime":self.end,
                           "unitGroup":"us",
                           "contentType":"csv",
                           "shortColumnNames":"0",
                           "timezone": timezone,
                           "extendedStats": 'true'}

        self.data = self.request_save()
        self.create_features()

    def request_save(self):
        self.response = requests.request("GET", url, headers=headers, params=self.querystring)

        try:
            self.ID = np.max([int(c.split('.')[0]) for c in os.listdir('DATA/weather')]) + 1
        except:
            self.ID = 1
        self.file = open(f'DATA/weather/{self.ID}.csv', 'wb')
        self.file.write(self.response.content)
        self.file.close()
        dat = pd.read_csv(f'DATA/weather/{self.ID}.csv').iloc[:-1, :]
        return dat

    def reverse_geocode(self):
        locator = Nominatim(user_agent = 'myGeocoder')
        self.location = locator.reverse(f'{self.lat}, {self.long}')

    def create_features(self):
        self.sunrise = self.owmData['srise_time']
        self.sunset = self.owmData['sset_time']
        self.data['timestamp'] = [dt.datetime.strptime(d, '%m/%d/%Y %H:%M:%S').timestamp() for d in self.data['Date time']]
        daylight = self.data[self.data['timestamp'] > self.sunrise]
        self.daylight = daylight[daylight['timestamp'] < self.sunset]

        self.avgTemp12 = self.data.loc[-12:,'Temperature'].mean()
        self.maxTemp12 = self.data.loc[-12:,'Temperature'].max()
        self.minTemp12 = self.data.loc[-12:,'Temperature'].min()
        self.solarTime = np.sum(5-self.data.loc[self.daylight.index, 'Cloud Cover'])
        self.windspeed = self.owmData['wnd']['speed']





def retrieve_weather(lat, long, ts):
    MW = MasterWeather(lat, long, ts)
    master = {}
    for att in dir(MW):
        if '__' in att:
            continue
        if type(getattr(MW, att)) == types.MethodType:
            continue
        if type(getattr(MW, att)) == dict and att == 'owmData':
            for name, dat in getattr(MW, att).items():
                master[name] = dat
        else:
            try:
                len(getattr(MW, att))
            except:
                master[att] = getattr(MW, att)
    return master


retrieve_weather(30, 30, (dt.datetime.today()-dt.timedelta(1)).timestamp())


