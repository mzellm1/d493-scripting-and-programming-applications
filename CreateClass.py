class WeatherLoc:
    def __init__(self, latitude, longitude, month, day, year,
                 avg_temp, min_temp, max_temp, avg_wind_speed,
                 min_wind_speed, max_wind_speed, sum_precipitation,
                 min_precipitation, max_precipitation):
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year
        self.avg_temperature = avg_temp
        self.min_temperature = min_temp
        self.max_temperature = max_temp
        self.avg_wind_speed = avg_wind_speed
        self.min_wind_speed = min_wind_speed
        self.max_wind_speed = max_wind_speed
        self.sum_precipitation = sum_precipitation
        self.min_precipitation = min_precipitation
        self.max_precipitation = max_precipitation

        print(f"Latitude: {self.latitude}")  # Adding print statements for testing purposes
        print(f"Longitude: {self.longitude}")
        print(f"Month: {self.month}")
        print(f"Day: {self.day}")
        print(f"Year: {self.year}")
        print(f"Average Temperature: {self.avg_temperature}")
        print(f"Minimum Temperature: {self.min_temperature}")
        print(f"Maximum Temperature: {self.max_temperature}")
        print(f"Average Wind Speed: {self.avg_wind_speed}")
        print(f"Minimum Wind Speed: {self.min_wind_speed}")
        print(f"Maximum Wind Speed: {self.max_wind_speed}")
        print(f"Sum Precipitation: {self.sum_precipitation}")
        print(f"Minimum Precipitation: {self.min_precipitation}")
        print(f"Maximum Precipitation: {self.max_precipitation}")
        print("WeatherLoc instance created successfully!\n")

# test


TestWeather = WeatherLoc(
    latitude=42,
    longitude=-107,
    month=7,
    day=3,
    year=2012,
    avg_temp=102,
    min_temp=92,
    max_temp=114,
    avg_wind_speed=8.0,
    min_wind_speed=1.0,
    max_wind_speed=22.0,
    sum_precipitation=14.0,
    min_precipitation=1.0,
    max_precipitation=13.0
)

print(TestWeather)
