"""
Flask Web Application for Travel Recommendation System
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import pandas as pd
from travel_planner import TravelPlanner
from route_optimizer import optimize_route, calculate_distance

app = Flask(__name__)
CORS(app)

# Initialize travel planner
planner = TravelPlanner()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get travel recommendations"""
    try:
        data = request.json
        user_name = data.get('name', 'Traveler')
        destination = data.get('city', 'vancouver').lower()
        days = int(data.get('days', 3))
        
        # Calculate dates
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days-1)
        
        # Budget
        total_budget = float(data.get('budget', 1000))
        budget = {
            'total': total_budget,
            'hotel': total_budget * 0.4,
            'attractions': total_budget * 0.3,
            'food': total_budget * 0.3
        }
        
        # Preferences
        preferences = {
            'attraction_categories': {
                'tours_&_sightseeing': 4.0,
                'outdoor_activities': 5.0,
                'cultural_&_theme_tours': 4.0
            },
            'hotel_amenities': [
                "Nonsmoking hotel",
                "Family Rooms",
                "Public Wifi",
                "Air conditioning",
                "Free parking"
            ],
            'cuisine_preferences': ['Local', 'Italian', 'Asian'],
            'activity_interests': ['outdoor', 'cultural', 'food']
        }
        
        # Get recommendations
        plan = planner.create_travel_plan(
            user_name=user_name,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            preferences=preferences
        )
        
        # Prepare response with locations for map
        response = {
            'success': True,
            'user_name': user_name,
            'destination': destination,
            'days': days,
            'plan': plan,
            'locations': extract_locations(plan),
            'route': calculate_route(plan)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def extract_locations(plan):
    """Extract all locations from the plan for map display"""
    locations = []
    
    # Hotels
    for hotel in plan.get('hotels', []):
        lat = hotel.get('latitude', 0)
        lng = hotel.get('longitude', 0)
        # If no coordinates, try to get from dataset
        if lat == 0 and lng == 0:
            coords = get_hotel_coordinates(hotel.get('name', ''), hotel.get('address', ''))
            if coords:
                lat, lng = coords
        
        if lat != 0 and lng != 0:
            locations.append({
                'name': hotel.get('name', 'Hotel'),
                'type': 'hotel',
                'lat': lat,
                'lng': lng,
                'price': hotel.get('price', 0),
                'rating': hotel.get('rating', 0),
                'address': hotel.get('address', '')
            })
    
    # Attractions (from attractions dict)
    attractions_dict = plan.get('attractions', {})
    for day_key, day_attractions in attractions_dict.items():
        for time_slot in ['morning', 'evening']:
            for attraction in day_attractions.get(time_slot, []):
                if attraction.get('latitude') and attraction.get('longitude'):
                    locations.append({
                        'name': attraction.get('name', 'Attraction'),
                        'type': 'attraction',
                        'lat': float(attraction.get('latitude', 0)),
                        'lng': float(attraction.get('longitude', 0)),
                        'price': float(attraction.get('price', 0)),
                        'rating': float(attraction.get('rating', 0)),
                        'day': day_key,
                        'time': time_slot
                    })
    
    # Restaurants
    for day_key, day_restaurants in plan.get('restaurants', {}).items():
        for meal_type, restaurants in day_restaurants.items():
            for restaurant in restaurants:
                if 'latitude' in restaurant and 'longitude' in restaurant:
                    locations.append({
                        'name': restaurant.get('name', 'Restaurant'),
                        'type': 'restaurant',
                        'lat': restaurant.get('latitude', 0),
                        'lng': restaurant.get('longitude', 0),
                        'price': restaurant.get('price', 0),
                        'rating': restaurant.get('rating', 0),
                        'meal': meal_type,
                        'day': day_key
                    })
    
    return locations

def calculate_route(plan):
    """Calculate optimized route for map display"""
    locations = extract_locations(plan)
    
    if len(locations) < 2:
        return []
    
    # Group by day if available
    locations_by_day = {}
    for loc in locations:
        day = loc.get('day', 'Day 1')
        if day not in locations_by_day:
            locations_by_day[day] = []
        locations_by_day[day].append(loc)
    
    # Optimize route for each day
    routes = {}
    for day, day_locations in locations_by_day.items():
        if len(day_locations) > 1:
            # Convert to format for optimizer
            locs_for_opt = [{'latitude': l['lat'], 'longitude': l['lng'], **l} 
                           for l in day_locations]
            optimized, total_dist = optimize_route(locs_for_opt)
            routes[day] = {
                'locations': optimized,
                'total_distance_km': total_dist
            }
        else:
            routes[day] = {
                'locations': day_locations,
                'total_distance_km': 0
            }
    
    return routes

def get_hotel_coordinates(hotel_name, address):
    """Get hotel coordinates from dataset"""
    try:
        # Try to load hotel data
        import glob
        files = glob.glob('etl/del_dup/*.json')
        for f in files[:5]:  # Check first few files
            with open(f, 'r') as file:
                for line in file:
                    try:
                        data = json.loads(line)
                        if 'hotel_name' in data and data['hotel_name'] == hotel_name:
                            if 'location' in data:
                                loc = data['location']
                                if isinstance(loc, str):
                                    # Parse string like "[lat, lon]"
                                    loc = eval(loc)
                                if len(loc) >= 2:
                                    return [float(loc[0]), float(loc[1])]
                    except:
                        continue
    except:
        pass
    return None

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get list of available cities"""
    cities = [
        {'name': 'Vancouver', 'value': 'vancouver', 'hotels': 27},
        {'name': 'Quebec', 'value': 'quebec', 'hotels': 752},
        {'name': 'Saskatoon', 'value': 'saskatoon', 'hotels': 54},
        {'name': 'Halifax', 'value': 'halifax', 'hotels': 46},
        {'name': 'Montreal', 'value': 'montreal', 'hotels': 3},
        {'name': 'Toronto', 'value': 'toronto', 'hotels': 5},
        {'name': 'Victoria', 'value': 'victoria', 'hotels': 29},
        {'name': 'Banff', 'value': 'banff', 'hotels': 21},
        {'name': 'Calgary', 'value': 'calgary', 'hotels': 1},
        {'name': 'Ottawa', 'value': 'ottawa', 'hotels': 3}
    ]
    return jsonify(cities)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Changed to 5001 to avoid AirPlay conflict
    print(f"\n🌍 Server starting on http://localhost:{port}")
    print("📱 Open this URL in your browser\n")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)  # Disable reloader to avoid import issues

