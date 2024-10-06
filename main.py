import requests

# C.1.
# noinspection PyShadowingNames


class WeatherLoc:
    def __init__(self, mlatitude, mlongitude, month, day, year,
                 maveragetemp, mtempmin, mtempmax, maveragewindspeed,
                 mwindspeedmin, mwindspeedmax, msumprecipitation,
                 mrainmin, mrainmax):
        self.mlatitude = mlatitude
        self.mlongitude = mlongitude
        self.month = month
        self.day = day
        self.year = year
        self.maveragetemp = maveragetemp
        self.mtempmin = mtempmin
        self.mtempmax = mtempmax
        self.maveragewindspeed = maveragewindspeed
        self.mwindspeedmin = mwindspeedmin
        self.mwindspeedmax = mwindspeedmax
        self.msumprecipitation = msumprecipitation
        self.mrainmin = mrainmin
        self.mrainmax = mrainmax

# C.2.
# Conversion functions


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def ms_to_mph(meters_per_second):
    return meters_per_second * 2.23694


def mm_to_inches(mm):
    return mm / 25.4


# API URL
API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Location coordinates
LOCATION = {
    "latitude": 35.3395,  # Latitude for the location
    "longitude": -97.4867  # Longitude for the location
}


# Function to get the weather data for specific variables and location
def get_mean_temperature(date):
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "start_date": date,
        "end_date": date,
        "daily": "temperature_2m_mean",
        "timezone": "UTC"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "daily" in data and "temperature_2m_mean" in data["daily"]:
        temp_celsius = data["daily"]["temperature_2m_mean"][0]
        return celsius_to_fahrenheit(temp_celsius)
    return None


def get_max_wind_speed(date):
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "start_date": date,
        "end_date": date,
        "daily": "windspeed_10m_max",
        "timezone": "UTC"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "daily" in data and "windspeed_10m_max" in data["daily"]:
        wind_speed_ms = data["daily"]["windspeed_10m_max"][0]
        return ms_to_mph(wind_speed_ms)
    return None


def get_precipitation_sum(date):
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "start_date": date,
        "end_date": date,
        "daily": "precipitation_sum",
        "timezone": "UTC"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "daily" in data and "precipitation_sum" in data["daily"]:
        precipitation_mm = data["daily"]["precipitation_sum"][0]
        return mm_to_inches(precipitation_mm)
    return None


# Fetch weather data for May 20th for the last 5 years
# noinspection PyShadowingNames
def get_weather_for_last_5_years():
    # The years specified for clarity
    years = [2024, 2023, 2022, 2021, 2020]
    base_date = "05-20"
    weather_data = []

    for year in years:
        query_date = f"{year}-{base_date}"
        print(f"Fetching data for: {query_date}")  # Logging to confirm date being requested

        mean_temp = get_mean_temperature(query_date)
        max_wind_speed = get_max_wind_speed(query_date)
        precipitation_sum = get_precipitation_sum(query_date)

        # Check if the expected data was pulled
        print(
            f"Data received for {query_date}: Temp={mean_temp}, Wind={max_wind_speed}, "
            f"Precipitation={precipitation_sum}\n")

        weather_data.append({
            "date": query_date,
            "mean_temperature_fahrenheit": mean_temp,
            "max_wind_speed_mph": max_wind_speed,
            "precipitation_sum_inches": precipitation_sum
        })

    return weather_data


print("Data for each date is listed below.\n")

# Showing the data for May 20th over last 5 years
weather_data = get_weather_for_last_5_years()
for entry in weather_data:
    print(f"Date: {entry['date']}")
    print(f"Mean Temperature: {entry['mean_temperature_fahrenheit']}°F")
    print(f"Max Wind Speed: {entry['max_wind_speed_mph']} mph")
    print(f"Precipitation Sum: {entry['precipitation_sum_inches']} inches")
    print("-" * 30)

# C.3.

weather_data = get_weather_for_last_5_years()

# Create instances of WeatherLoc for May 20th date
weather_locations = []
latitude = 35.3395
longitude = -97.4867

for entry in weather_data:
    # Extract data for the WeatherLoc instance
    date_parts = entry['date'].split('-')
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])

    maveragetemp = entry['mean_temperature_fahrenheit']
    mtempmin = None
    mtempmax = None
    maveragewindspeed = entry['max_wind_speed_mph']
    mwindspeedmin = None
    mwindspeedmax = None
    msumprecipitation = entry['precipitation_sum_inches']
    mrainmin = None
    mrainmax = None

    # Create an instance of WeatherLoc
    weather_loc = WeatherLoc(
        mlatitude=latitude,
        mlongitude=longitude,
        month=month,
        day=day,
        year=year,
        maveragetemp=maveragetemp,
        mtempmin=mtempmin,
        mtempmax=mtempmax,
        maveragewindspeed=maveragewindspeed,
        mwindspeedmin=mwindspeedmin,
        mwindspeedmax=mwindspeedmax,
        msumprecipitation=msumprecipitation,
        mrainmin=mrainmin,
        mrainmax=mrainmax
    )

    # Append the instance to the list
    weather_locations.append(weather_loc)
