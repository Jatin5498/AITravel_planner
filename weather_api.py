"""
Weather API Integration Module
Provides real-time weather data for travel planning
"""
import requests
import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class WeatherAPI:
    """
    Weather API client using OpenWeatherMap
    Free tier: 60 calls/minute, 1,000,000 calls/month
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API
        
        Args:
            api_key: OpenWeatherMap API key (or set OPENWEATHER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, city: str, country_code: str = "CA") -> Dict:
        """
        Get current weather for a city
        
        Args:
            city: City name
            country_code: Country code (default: CA for Canada)
        
        Returns:
            Dictionary with weather data
        """
        if not self.api_key:
            return self._get_mock_weather(city)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{country_code}",
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'condition': data['weather'][0]['main'],
                'icon': data['weather'][0]['icon']
            }
        except Exception as e:
            print(f"⚠️  Weather API error: {e}. Using mock data.")
            return self._get_mock_weather(city)
    
    def get_forecast(self, city: str, days: int = 5, country_code: str = "CA") -> List[Dict]:
        """
        Get weather forecast for multiple days
        
        Args:
            city: City name
            days: Number of days to forecast (max 5 for free tier)
            country_code: Country code
        
        Returns:
            List of daily weather forecasts
        """
        if not self.api_key:
            return self._get_mock_forecast(city, days)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{city},{country_code}",
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 8 forecasts per day, max 40
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list'][:days * 8:8]:  # One per day
                forecasts.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d'),
                    'temperature': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'condition': item['weather'][0]['main'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                })
            
            return forecasts
        except Exception as e:
            print(f"⚠️  Weather API error: {e}. Using mock data.")
            return self._get_mock_forecast(city, days)
    
    def is_good_weather_for_activity(self, weather: Dict, activity_type: str) -> bool:
        """
        Determine if weather is suitable for an activity
        
        Args:
            weather: Weather data dictionary
            activity_type: 'outdoor', 'indoor', 'beach', 'hiking', etc.
        
        Returns:
            True if weather is suitable
        """
        condition = weather.get('condition', '').lower()
        temp = weather.get('temperature', 20)
        
        if activity_type == 'outdoor':
            return condition not in ['rain', 'storm', 'snow'] and temp > 5
        elif activity_type == 'beach':
            return condition == 'clear' and temp > 20
        elif activity_type == 'hiking':
            return condition not in ['rain', 'storm'] and 10 < temp < 30
        elif activity_type == 'indoor':
            return True  # Always suitable
        else:
            return True
    
    def _get_mock_weather(self, city: str) -> Dict:
        """Fallback mock weather data"""
        return {
            'city': city,
            'temperature': 20,
            'feels_like': 19,
            'description': 'partly cloudy',
            'humidity': 65,
            'wind_speed': 10,
            'condition': 'Clouds',
            'icon': '02d',
            'note': 'Mock data - API key not configured'
        }
    
    def _get_mock_forecast(self, city: str, days: int) -> List[Dict]:
        """Fallback mock forecast data"""
        forecasts = []
        for i in range(days):
            forecasts.append({
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'temperature': 20 + (i % 3) * 2,
                'description': 'partly cloudy',
                'condition': 'Clouds',
                'humidity': 65,
                'wind_speed': 10
            })
        return forecasts

