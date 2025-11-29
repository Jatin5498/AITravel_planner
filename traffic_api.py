"""
Traffic API Integration Module
Provides real-time traffic and route information
"""
import requests
import os
from typing import Dict, List, Optional, Tuple
from route_optimizer import calculate_distance, calculate_travel_time

class TrafficAPI:
    """
    Traffic and routing API client
    Uses OSRM (Open Source Routing Machine) as free alternative to Google Maps
    Can also use Google Maps Directions API if API key provided
    """
    
    def __init__(self, google_api_key: Optional[str] = None, use_osrm: bool = True):
        """
        Initialize Traffic API
        
        Args:
            google_api_key: Google Maps API key (optional)
            use_osrm: Use free OSRM service (default: True)
        """
        self.google_api_key = google_api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.use_osrm = use_osrm
        self.osrm_url = "http://router.project-osrm.org/route/v1"
    
    def get_route(self, origin: Tuple[float, float], destination: Tuple[float, float], 
                  mode: str = 'driving') -> Dict:
        """
        Get route between two points
        
        Args:
            origin: (latitude, longitude) of start point
            destination: (latitude, longitude) of end point
            mode: 'driving', 'walking', 'cycling'
        
        Returns:
            Dictionary with route information
        """
        if self.google_api_key and not self.use_osrm:
            return self._get_google_route(origin, destination, mode)
        else:
            return self._get_osrm_route(origin, destination, mode)
    
    def _get_osrm_route(self, origin: Tuple[float, float], destination: Tuple[float, float],
                       mode: str) -> Dict:
        """
        Get route using OSRM (free, no API key needed)
        """
        try:
            profile = 'driving' if mode == 'driving' else 'walking'
            url = f"{self.osrm_url}/{profile}/{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
            params = {
                'overview': 'false',
                'alternatives': 'false',
                'steps': 'false'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] == 'Ok' and len(data['routes']) > 0:
                route = data['routes'][0]
                distance_m = route['distance']
                duration_s = route['duration']
                
                return {
                    'distance_km': round(distance_m / 1000, 2),
                    'duration_minutes': round(duration_s / 60, 1),
                    'duration_seconds': duration_s,
                    'status': 'success',
                    'service': 'OSRM'
                }
            else:
                # Fallback to distance calculation
                return self._fallback_route(origin, destination, mode)
                
        except Exception as e:
            print(f"⚠️  OSRM API error: {e}. Using fallback calculation.")
            return self._fallback_route(origin, destination, mode)
    
    def _get_google_route(self, origin: Tuple[float, float], destination: Tuple[float, float],
                         mode: str) -> Dict:
        """
        Get route using Google Maps Directions API
        """
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {
                'origin': f"{origin[0]},{origin[1]}",
                'destination': f"{destination[0]},{destination[1]}",
                'mode': mode,
                'key': self.google_api_key
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK' and len(data['routes']) > 0:
                route = data['routes'][0]['legs'][0]
                return {
                    'distance_km': round(route['distance']['value'] / 1000, 2),
                    'duration_minutes': round(route['duration']['value'] / 60, 1),
                    'duration_seconds': route['duration']['value'],
                    'status': 'success',
                    'service': 'Google Maps'
                }
            else:
                return self._fallback_route(origin, destination, mode)
                
        except Exception as e:
            print(f"⚠️  Google Maps API error: {e}. Using fallback calculation.")
            return self._fallback_route(origin, destination, mode)
    
    def _fallback_route(self, origin: Tuple[float, float], destination: Tuple[float, float],
                       mode: str) -> Dict:
        """
        Fallback route calculation using straight-line distance
        """
        distance_km = calculate_distance(origin[0], origin[1], destination[0], destination[1])
        duration_minutes = calculate_travel_time(distance_km, mode)
        
        return {
            'distance_km': round(distance_km, 2),
            'duration_minutes': duration_minutes,
            'status': 'estimated',
            'service': 'fallback',
            'note': 'Using estimated distance and time'
        }
    
    def get_traffic_conditions(self, city: str) -> Dict:
        """
        Get current traffic conditions for a city
        Note: Full traffic data requires Google Maps API
        This is a simplified version
        
        Args:
            city: City name
        
        Returns:
            Dictionary with traffic information
        """
        # Simplified traffic conditions
        # In production, would use Google Maps Traffic API
        return {
            'city': city,
            'congestion_level': 'moderate',  # low, moderate, high
            'note': 'Traffic data requires Google Maps API. Using estimated values.'
        }
    
    def optimize_route_with_traffic(self, locations: List[Tuple[float, float]], 
                                   start: Tuple[float, float] = None) -> List[Tuple[float, float]]:
        """
        Optimize route considering traffic conditions
        
        Args:
            locations: List of (lat, lon) tuples
            start: Starting location
        
        Returns:
            Optimized route order
        """
        # For now, use basic route optimization
        # In production, would consider real-time traffic
        from route_optimizer import nearest_neighbor_route
        return nearest_neighbor_route(locations, start)

