APIKEY = '4e6392f3cf944a16b9012408210806'
from wwo_hist import retrieve_hist_data
import os

frequency = 3
start_date = '12-FEB-2021'
end_date = '13-FEB-2021'
location_list = ['singapore','california']
hist_weather_data = retrieve_hist_data(APIKEY,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)