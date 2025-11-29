"""
Route Optimization Module
Finds the most efficient travel path between recommended locations
"""
import math
from typing import List, Tuple, Dict
import pandas as pd
from geopy.distance import geodesic

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in kilometers
    """
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def nearest_neighbor_route(locations: List[Tuple[float, float]], start: Tuple[float, float] = None) -> List[int]:
    """
    Find route using Nearest Neighbor algorithm (simple TSP approximation)
    
    Args:
        locations: List of (latitude, longitude) tuples
        start: Starting location (if None, uses first location)
    
    Returns:
        List of indices representing the optimal route order
    """
    if not locations:
        return []
    
    if len(locations) == 1:
        return [0]
    
    n = len(locations)
    unvisited = set(range(n))
    route = []
    
    # Start from first location or specified start
    if start:
        # Find closest location to start
        current = min(range(n), key=lambda i: calculate_distance(start[0], start[1], 
                                                                 locations[i][0], locations[i][1]))
    else:
        current = 0
    
    route.append(current)
    unvisited.remove(current)
    
    # Greedily visit nearest unvisited location
    while unvisited:
        nearest = min(unvisited, key=lambda i: calculate_distance(
            locations[current][0], locations[current][1],
            locations[i][0], locations[i][1]
        ))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    return route

def optimize_route(locations: List[Dict], start_location: Tuple[float, float] = None) -> List[Dict]:
    """
    Optimize route for a list of locations with metadata
    
    Args:
        locations: List of dicts with 'latitude', 'longitude', and other metadata
        start_location: Optional starting point (lat, lon)
    
    Returns:
        List of locations in optimized order
    """
    if not locations:
        return []
    
    # Extract coordinates
    coords = [(loc.get('latitude', 0), loc.get('longitude', 0)) for loc in locations]
    
    # Get optimized route order
    route_order = nearest_neighbor_route(coords, start_location)
    
    # Reorder locations according to optimized route
    optimized = [locations[i] for i in route_order]
    
    # Calculate total distance
    total_distance = 0
    for i in range(len(optimized) - 1):
        loc1 = optimized[i]
        loc2 = optimized[i + 1]
        dist = calculate_distance(
            loc1.get('latitude', 0), loc1.get('longitude', 0),
            loc2.get('latitude', 0), loc2.get('longitude', 0)
        )
        total_distance += dist
        optimized[i]['distance_to_next'] = round(dist, 2)
    
    if len(optimized) > 0:
        optimized[-1]['distance_to_next'] = 0
    
    return optimized, total_distance

def cluster_by_proximity(locations: List[Dict], max_distance_km: float = 5.0) -> List[List[Dict]]:
    """
    Cluster locations by proximity for efficient day planning
    
    Args:
        locations: List of location dicts
        max_distance_km: Maximum distance for clustering
    
    Returns:
        List of clusters (each cluster is a list of nearby locations)
    """
    if not locations:
        return []
    
    clusters = []
    unassigned = locations.copy()
    
    while unassigned:
        # Start new cluster with first unassigned location
        cluster = [unassigned.pop(0)]
        cluster_center = (cluster[0].get('latitude', 0), cluster[0].get('longitude', 0))
        
        # Find nearby locations
        i = 0
        while i < len(unassigned):
            loc = unassigned[i]
            dist = calculate_distance(
                cluster_center[0], cluster_center[1],
                loc.get('latitude', 0), loc.get('longitude', 0)
            )
            
            if dist <= max_distance_km:
                cluster.append(unassigned.pop(i))
            else:
                i += 1
        
        clusters.append(cluster)
    
    return clusters

def calculate_travel_time(distance_km: float, mode: str = 'driving') -> float:
    """
    Estimate travel time based on distance and mode
    
    Args:
        distance_km: Distance in kilometers
        mode: 'driving', 'walking', 'transit'
    
    Returns:
        Estimated time in minutes
    """
    # Average speeds (km/h)
    speeds = {
        'driving': 50,
        'walking': 5,
        'transit': 30,
        'cycling': 15
    }
    
    speed = speeds.get(mode, 50)
    time_hours = distance_km / speed
    return round(time_hours * 60, 1)  # Convert to minutes

