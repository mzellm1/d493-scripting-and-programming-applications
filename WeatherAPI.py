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

# Testing
weather_data = get_weather_for_last_5_years()
for entry in weather_data:
    print(f"Date: {entry['date']}")
    print(f"Mean Temperature: {entry['mean_temperature_fahrenheit']}°F")
    print(f"Max Wind Speed: {entry['max_wind_speed_mph']} mph")
    print(f"Precipitation Sum: {entry['precipitation_sum_inches']} inches")
    print("-" * 30)

# noinspection PyShadowingNames


def get_temperature_data(date):
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "start_date": date,
        "end_date": date,
        "daily": ["temperature_2m_min", "temperature_2m_max", "temperature_2m_mean"],
        "timezone": "UTC"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "daily" in data:
        temp_min = data["daily"].get("temperature_2m_min", [None])[0]
        temp_max = data["daily"].get("temperature_2m_max", [None])[0]
        temp_mean = data["daily"].get("temperature_2m_mean", [None])[0]
        return (
            celsius_to_fahrenheit(temp_mean) if temp_mean else None,
            celsius_to_fahrenheit(temp_min) if temp_min else None,
            celsius_to_fahrenheit(temp_max) if temp_max else None
        )
    return None, None, None

def get_wind_speed_data(date):
    params = {
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "start_date": date,
        "end_date": date,
        "daily": ["windspeed_10m_max", "windspeed_10m_mean", "windspeed_10m_min"],
        "timezone": "UTC"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "daily" in data:
        wind_speed_mean = data["daily"].get("windspeed_10m_mean", [None])[0]
        wind_speed_min = data["daily"].get("windspeed_10m_min", [None])[0]
        wind_speed_max = data["daily"].get("windspeed_10m_max", [None])[0]
        return (
            ms_to_mph(wind_speed_mean) if wind_speed_mean else None,
            ms_to_mph(wind_speed_min) if wind_speed_min else None,
            ms_to_mph(wind_speed_max) if wind_speed_max else None
        )
    return None, None, None

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

def get_weather_for_last_5_years(session):
    years = [2024, 2023, 2022, 2021, 2020]
    base_date = "05-20"  # Target date

    for year in years:
        query_date = f"{year}-{base_date}"
        print(f"Fetching data for: {query_date}")

        # Fetch data
        mean_temp, min_temp, max_temp = get_temperature_data(query_date)
        avg_wind_speed, min_wind_speed, max_wind_speed = get_wind_speed_data(query_date)
        precipitation_sum = get_precipitation_sum(query_date)

        # Create a new record
        new_record = WeatherLoc(
            latitude=35.3395,
            longitude=-97.4867,
            month=5,
            day=20,
            year=year,
            avg_temperature=mean_temp,
            min_temperature=min_temp,
            max_temperature=max_temp,
            avg_wind_speed=avg_wind_speed,
            min_wind_speed=min_wind_speed,
            max_wind_speed=max_wind_speed,
            sum_precipitation=precipitation_sum,
            min_precipitation=None,
            max_precipitation=None
        )

        # Add the record to the session
        session.add(new_record)

    # Commit the session to save all records
    session.commit()


DATABASE_URL = "sqlite:///weather_data.db"
engine = create_engine(DATABASE_URL)

# Drop the existing table if it exists
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS weather_data;"))

Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all records from the WeatherData table
# noinspection PyShadowingNames


def fetch_and_print_weather_data(session):
    records = session.query(WeatherLoc).all()

    # Print headers
    headers = [
        "ID", "Latitude", "Longitude", "Year", "Month", "Day",
        "Avg Temp (°F)", "Min Temp (°F)", "Max Temp (°F)",
        "Avg Wind Speed (mph)", "Min Wind Speed (mph)", "Max Wind Speed (mph)",
        "Total Precipitation (in)", "Min Precipitation (in)", "Max Precipitation (in)"
    ]

    # Define a header format to ensure the headers align with the data
    header_format = ("{:<5} | {:<9} | {:<10} | {:<5} | {:<6} | {:<4} | {:<14} | {:<14} | {:<14} | {:<20} | "
                     "{:<20} | {:<20} | {:<23} | {:<23} | {:<23}")

    # Print the header row
    print(header_format.format(*headers))
    print('-' * 180)

    # Define a data format to align the data with the headers
    data_format = ("{:<5} | {:<9} | {:<10} | {:<5} | {:<6} | {:<4} | {:<14} | {:<14} | {:<14} | {:<20} | "
                   "{:<20} | {:<20} | {:<23} | {:<23} | {:<23}")

    # Print each record
    for record in records:
        print(data_format.format(
            record.id or "N/A",
            f"{record.latitude:.2f}" if record.latitude is not None else "N/A",
            f"{record.longitude:.2f}" if record.longitude is not None else "N/A",
            record.year or "N/A",
            record.month or "N/A",
            record.day or "N/A",
            f"{record.avg_temperature:.2f}" if record.avg_temperature is not None else "N/A",
            f"{record.min_temperature:.2f}" if record.min_temperature is not None else "N/A",
            f"{record.max_temperature:.2f}" if record.max_temperature is not None else "N/A",
            f"{record.avg_wind_speed:.2f}" if record.avg_wind_speed is not None else "N/A",
            f"{record.min_wind_speed:.2f}" if record.min_wind_speed is not None else "N/A",
            f"{record.max_wind_speed:.2f}" if record.max_wind_speed is not None else "N/A",
            f"{record.sum_precipitation:.2f}" if record.sum_precipitation is not None else "N/A",
            f"{record.min_precipitation:.2f}" if record.min_precipitation is not None else "N/A",
            f"{record.max_precipitation:.2f}" if record.max_precipitation is not None else "N/A"
        ))


# Call the function to fetch and print data
get_weather_for_last_5_years(session)

fetch_and_print_weather_data(session)
