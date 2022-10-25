from pyowm.owm import OWM
from pyowm.utils.config import get_config_from
from config import APIKEY
from pyowm.utils.config import get_default_config_for_subscription_type
from pyowm.utils import timestamps, formatting
import types
import datetime as dt
'''CONSTANTS'''
owmAPIKEY = '6bc99af9eed4d9fd483b60f6d3229651'

class OwmWeather:
    def __init__(self, timestamp, lat, long):
        self.time = int(timestamp)
        self.lat = lat
        self.long = long
        config_dict = get_default_config_for_subscription_type('developer')
        owm = OWM(owmAPIKEY, config_dict)
        mgr = owm.weather_manager()
        oneCallData = mgr.one_call_history(lat=self.lat, lon=self.long, dt=self.time).current
        atts = [c for c in dir(oneCallData) if '_' != c[0]]
        self.owmData = {}
        for att in atts:
            if not isinstance(getattr(oneCallData, att), types.MethodType):
                self.owmData[att] = getattr(oneCallData, att)

    def weather_data(self):
        oneCallData = self.mgr.one_call_history(lat=self.lat, lon=self.long, dt=self.time).current
        atts = [c for c in dir(oneCallData) if '_' != c[0]]
        self.owmData = {}
        for att in atts:
            if not isinstance(getattr(oneCallData, att), types.MethodType):
                self.owmData[att] = getattr(oneCallData, att)
        return self.owmData

    def accumulation(self):
        return

    def statistical(self):
        return

# lat, long, year = 33.2164, -97.1292, 2010
# dd = Weather(int(dt.datetime.today().timestamp()), lat ,long)
# print(dd.weather_data())
