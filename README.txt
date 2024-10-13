Python project:
Dates - May 20th 2012-2017
Location – Moore, OK
Latitude and Longitude - 35.3395° N, 97.4867° W

This program uses multiple classes and functions in order to run properly. WeatherLoc (weather location shorted for
convivence) is the first class create and contains information for a weather location’s latitude, longitude, month,
day, year, average temperature, minimum temperature, maximum temperature, average windspeed, minimum windspeed,
maximum windspeed, sum of precipitation, minimum precipitation, and the maximum precipitation.

WeatherLoc is set with a declarative base in the ClassForSQLA file so that it can work within the Weather API and
SQL Alchemy database as a table.

The URL to use for the weather API function to pull accurate data is https://archive-api.open-meteo.com/v1/archive.

Three functions are used specifically to pull the data requested by this project. There’s a function gathering the
sum of participation across the five days data is being pulled on named precipitation_sum. Another function for finding
the max wind speed on those days named max_wind_speed. And the third is for finding the mean temperature on those days
called mean_temp.

There is a function that uses those three functions listed above to actually go and pull the data from the website and
returns it in weather_data to be used in the program. It is coded as:

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


After being run to access the data from the API, the get_weather_for_last_5_years function gets created again with a
session call, get_weather_for_last_5_years(session) so it is able to access the table in SQL Alchemy. The function
creates a record named new_record and adds the record to the session and then commits the session to save all the records.

The database URL is "sqlite:///weather_data.db". Since this code is creating the table it also drops the table if it
already exists to avoid redundancy with the data. Once the table and record has been committed, a function is used to
fetch the data. The function is named fetch_and_print_weather_data(session). This function pulls the necessary data and
puts it into a table and then prints the table when the function is called.

For the functions and classes to work properly, imports will be necessary. First import requests, then from sqlalchemy
import create_engine and text, then from sqlalchemy.orm import sessionmaker, and then assuming the WeatherLoc(Base)
class is in a separate file it will need to set up as from ClassForSQLA import WeatherLoc, Base. If the class is created
in the same file like it is in main.py then that import will not be necessary.

At the bottom of the code there are two functions called in order to pull the data, create a record and table, and then
pull the data and print the table. They are called in order:

get_weather_for_last_5_years(session)

fetch_and_print_weather_data(session)

This results in a table with headers printed and the only fields filled in are the required fields for this project:
precipitation_sum, max_wind_speed, and mean_temp.
