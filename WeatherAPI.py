import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ClassForSQLA import WeatherLoc, Base


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
            f"Data received for {query_date}: Temp={mean_temp}, Wind={max_wind_speed}, Precipitation={precipitation_sum}\n")

        weather_data.append({
            "date": query_date,
            "mean_temperature_fahrenheit": mean_temp,
            "max_wind_speed_mph": max_wind_speed,
            "precipitation_sum_inches": precipitation_sum
        })

    return weather_data


print("Data for each date is listed below.\n")

# Testing
weather_data = get_weather_for_last_5_years()
for entry in weather_data:
    print(f"Date: {entry['date']}")
    print(f"Mean Temperature: {entry['mean_temperature_fahrenheit']}°F")
    print(f"Max Wind Speed: {entry['max_wind_speed_mph']} mph")
    print(f"Precipitation Sum: {entry['precipitation_sum_inches']} inches")
    print("-" * 30)

# Main script


def get_weather_for_last_5_years(session):
    years = [2024, 2023, 2022, 2021, 2020]
    base_date = "05-20"  # Target date

    for year in years:
        query_date = f"{year}-{base_date}"
        print(f"Fetching data for: {query_date}")

        # Fetch data
        mean_temp = get_mean_temperature(query_date)
        max_wind_speed = get_max_wind_speed(query_date)
        precipitation_sum = get_precipitation_sum(query_date)

        # Create a new record
        new_record = WeatherLoc(
            latitude=35.3395,  # Your actual latitude
            longitude=-97.4867,  # Your actual longitude
            month=5,
            day=20,
            year=year,
            avg_temperature=mean_temp,
            min_temperature=None,
            max_temperature=None,
            avg_wind_speed=None,
            min_wind_speed=None,
            max_wind_speed=max_wind_speed,
            sum_precipitation=precipitation_sum,
            min_precipitation=None,
            max_precipitation=None
        )

        # Add the record to the session
        session.add(new_record)

    # Commit the session to save all records
    session.commit()

DATABASE_URL = "sqlite:///weather_data.db"  # Update with your actual database path
engine = create_engine(DATABASE_URL)

# Drop the existing table if it exists
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS weather_data;"))

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch weather data and insert it into the database


# Fetch all records from the WeatherData table
def fetch_and_print_weather_data(session):
    records = session.query(WeatherLoc).all()

    # Print headers
    headers = [
        "ID", "Latitude", "Longitude", "Year", "Month", "Day",
        "Avg Temp (°F)", "Min Temp (°F)", "Max Temp (°F)",
        "Avg Wind Speed (mph)", "Min Wind Speed (mph)", "Max Wind Speed (mph)",
        "Total Precipitation (in)", "Min Precipitation (in)", "Max Precipitation (in)"
    ]

    print(f"{' | '.join(headers)}")
    print('-' * 100)

    # Print each record
    for record in records:
        print(f"{record.id} | {record.latitude} | {record.longitude} | "
              f"{record.year} | {record.month} | {record.day} | "
              f"{record.avg_temperature} | {record.min_temperature} | {record.max_temperature} | "
              f"{record.avg_wind_speed} | {record.min_wind_speed} | {record.max_wind_speed} | "
              f"{record.sum_precipitation} | {record.min_precipitation} | {record.max_precipitation}")


# Call the function to fetch and print data
get_weather_for_last_5_years(session)

fetch_and_print_weather_data(session)
