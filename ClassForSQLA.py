from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WeatherLoc(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    avg_temperature = Column(Float, nullable=True)
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    avg_wind_speed = Column(Float, nullable=True)
    min_wind_speed = Column(Float, nullable=True)
    max_wind_speed = Column(Float, nullable=True)
    sum_precipitation = Column(Float, nullable=True)
    min_precipitation = Column(Float, nullable=True)
    max_precipitation = Column(Float, nullable=True)

    def __init__(self, latitude, longitude, month, day, year,
                 avg_temperature=None, min_temperature=None, max_temperature=None,
                 avg_wind_speed=None, min_wind_speed=None, max_wind_speed=None,
                 sum_precipitation=None, min_precipitation=None, max_precipitation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year
        self.avg_temperature = avg_temperature
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.avg_wind_speed = avg_wind_speed
        self.min_wind_speed = min_wind_speed
        self.max_wind_speed = max_wind_speed
        self.sum_precipitation = sum_precipitation
        self.min_precipitation = min_precipitation
        self.max_precipitation = max_precipitation
