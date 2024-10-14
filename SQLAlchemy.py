import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ClassForSQLA import WeatherLoc, Base


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
