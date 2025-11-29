"""
Configuration file for API keys and settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (set these in .env file or environment variables)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# Default settings
DEFAULT_CITY = "vancouver"
DEFAULT_DAYS = 3
DEFAULT_BUDGET = 1000.0

# Route optimization settings
MAX_DISTANCE_FOR_CLUSTERING = 5.0  # km
DEFAULT_TRAVEL_MODE = 'driving'  # driving, walking, transit, cycling

# Weather settings
WEATHER_UNIT = 'metric'  # metric or imperial
WEATHER_FORECAST_DAYS = 5

# Restaurant settings
RESTAURANT_RECOMMENDATIONS_PER_MEAL = 2
DEFAULT_CUISINES = ['Local', 'Italian', 'Asian', 'Mexican', 'American']

# Attraction settings
ATTRACTIONS_PER_TIME_SLOT = 2  # Morning and Evening
DEFAULT_ATTRACTION_CATEGORIES = {
    'tours_&_sightseeing': 4.0,
    'outdoor_activities': 5.0,
    'cultural_&_theme_tours': 4.0
}

# Hotel settings
HOTEL_RECOMMENDATIONS_COUNT = 5
DEFAULT_HOTEL_AMENITIES = [
    "Nonsmoking hotel",
    "Family Rooms",
    "Public Wifi",
    "Air conditioning",
    "Free parking"
]

