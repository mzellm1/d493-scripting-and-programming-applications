
import requests
from datetime import datetime


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
