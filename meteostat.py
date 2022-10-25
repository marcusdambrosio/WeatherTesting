from datetime import datetime
import meteostat

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2018, 12, 31, 23, 59)

# Get hourly data
data = meteostat.Hourly('72219', start, end)
data = data.fetch()

# Print DataFrame
print(data)
