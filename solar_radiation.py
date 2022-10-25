import pandas as pd
import numpy as np
import sys, os
import datetime as dt
import datetime as dt
from pyowmap import owmAPIKEY, owmWeather
# Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
# Define the lat, long of the location and the year

'''CONSTANTS'''
APIKEY = 'rS4tvImJK1vSQLMRwJRiHYjvQAaAIrXI7vm8ZkGX'
attributes = 'air_temperature,cloud_type,dew_point,' \
             'ghi,dhi,dni,solar_zenith_angle,fill_flag,' \
             'relative_humidity,surface_albedo,surface_pressure,' \
             'total_precipitable_water,wind_direction,wind_speed'
'''
cloud_type: outputs an integer that im assuming corresponds to a type of cloud
ghi: Global horizontal irradiance -- amount of radiation falling on a surface horizontal to the surface of the earth
dhi: Diffuse horizontal irradiance -- amount of radiation received per unit area by a surface 
dni: Direct noramal irradiance -- amount of radiation recieved per unit area by a surface perpendicular to solar rays
solar_zenith_angle: angle between the sun's rays and the vertical direction
fill_flag: not sure about this? Outputs integers in [0,1,3,4] 
surface_albedo: fraction of sunlight reflected by the surface of the earth
total_precipitable_water: the amount of water in the atmosphere that can be obtained if all had condensed to liquid
'''
leapYear = 'false'
interval = '30'
utc = 'true'
name = 'Marcus+Dambrosio'
reason = 'research'
company = 'Exchange+Bees'
email = 'marcues@exchangebees.com'
mailing = 'false'


lat, lon, year = 33.2164, -97.1292, 2010


class Weather(owmWeather):
    def __init__(self, timestamp, lat, long):
        super().__init__(timestamp, lat, long)
        self.year = dt.datetime.utcfromtimestamp(timestamp).year
        self.lat = lat
        self.long = long
        self.url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
            year=self.year, lat=self.lat, lon=self.long, leap=leapYear, interval=interval, utc=utc,
            name=name, email=email, mailing_list=mailing, affiliation=company, reason=reason, api=APIKEY,
            attr=attributes)
        self.data = pd.read_csv(self.url)
        self.metadata = {}
        for i in range(len(self.data.columns)):
            self.metadata[self.data.columns[i]] = self.data.iloc[0, i]
        self.data.columns = self.data.iloc[1, :]
        self.data = self.data.iloc[2:, :].dropna(axis = 1).reset_index()
        self.format_datetime()


    def format_datetime(self):
        self.datetime = []
        for i in range(len(self.data)):
            self.datetime.append(dt.datetime(year = int(self.data.Year[i]), month = int(self.data.Month[i]), day = int(self.data.Day[i]),
                                            hour = int(self.data.Hour[i]), minute = int(self.data.Minute[i])))
        self.data['datetime'] = self.datetime


dd = Weather(dt.datetime(year = 2020,month = 6,day = 20).timestamp(), lat, lon)
print(dd.weatherData)
# Declare url string
# url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(
#     year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email,
#     mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=APIKEY, attr=attributes)# Return just the first 2 lines to get metadata:
# df = pd.read_csv(url, skiprows = 2)

# print(df.columns)


sys.exit()
df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval + 'Min', periods=525600 / int(interval)), inplace = True)
df.to_excel('solar_data.xlsx')
# See metadata for specified properties, e.g., timezone and elevation
# timezone, elevation = info['Local Time Zone'], info['Elevation']