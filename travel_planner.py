"""
Comprehensive Travel Plan Generator
Combines attractions, hotels, restaurants, and route optimization
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
# Import hotel functions conditionally (only when Spark is available)
# from hotel_recc import amenities_rating, model_train, get_hotel_recc
from restaurant_recommender import RestaurantRecommender
from route_optimizer import optimize_route, cluster_by_proximity, calculate_travel_time
from weather_api import WeatherAPI
from traffic_api import TrafficAPI

# Import attraction functions at module level
ATTRACTION_MODULE_AVAILABLE = True
_module_get_recc = None
_module_filter_df = None

try:
    import attractions_recc
    _module_get_recc = getattr(attractions_recc, 'get_recc', None)
    _module_filter_df = getattr(attractions_recc, 'filter_df', None)
    if _module_get_recc is None or _module_filter_df is None:
        ATTRACTION_MODULE_AVAILABLE = False
except Exception as e:
    print(f"⚠️  Attraction recommendation module not available: {e}")
    ATTRACTION_MODULE_AVAILABLE = False

# Conditional PySpark imports
try:
    import pyspark
    from pyspark.sql import SQLContext
    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False
    pyspark = None
    SQLContext = None

class TravelPlanner:
    """
    Main travel planning system that integrates all components
    """
    
    def __init__(self):
        """Initialize travel planner with all components"""
        self.weather_api = WeatherAPI()
        self.traffic_api = TrafficAPI()
        self.restaurant_recommender = RestaurantRecommender()
        self.spark = None
        
    def initialize_spark(self):
        """Initialize PySpark for hotel recommendations"""
        if not PYSPARK_AVAILABLE:
            return False
            
        import os
        java17_home = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
        if os.path.exists(java17_home):
            os.environ['JAVA_HOME'] = java17_home
            os.environ['PATH'] = f"{java17_home}/bin:{os.environ.get('PATH', '')}"
        
        try:
            if not PYSPARK_AVAILABLE:
                return False
            sc = pyspark.SparkContext(appName="travel_planner")
            self.spark = SQLContext(sc)
            return True
        except Exception as e:
            print(f"⚠️  PySpark initialization failed: {e}")
            return False
    
    def create_travel_plan(self, 
                          user_name: str,
                          destination: str,
                          start_date: datetime.date,
                          end_date: datetime.date,
                          budget: Dict[str, float],
                          preferences: Dict) -> Dict:
        """
        Create comprehensive travel plan
        
        Args:
            user_name: User's name
            destination: Destination city
            start_date: Trip start date
            end_date: Trip end date
            budget: {'total': float, 'hotel': float, 'attractions': float, 'food': float}
            preferences: {
                'attraction_categories': dict,
                'hotel_amenities': list,
                'cuisine_preferences': list,
                'activity_interests': list
            }
        
        Returns:
            Complete travel plan dictionary
        """
        days = (end_date - start_date).days + 1
        
        print("=" * 70)
        print("🌍 COMPREHENSIVE TRAVEL PLAN GENERATOR")
        print("=" * 70)
        print(f"\n📍 Destination: {destination.title()}")
        print(f"📅 Duration: {days} days ({start_date} to {end_date})")
        print(f"💰 Budget: ${budget.get('total', 0):.2f}")
        
        plan = {
            'user_name': user_name,
            'destination': destination,
            'start_date': str(start_date),
            'end_date': str(end_date),
            'days': days,
            'budget': budget,
            'weather': {},
            'hotels': [],
            'attractions': {},
            'restaurants': {},
            'daily_itinerary': {},
            'route_optimization': {}
        }
        
        # Step 1: Get weather forecast
        print("\n" + "=" * 70)
        print("STEP 1: Getting Weather Forecast")
        print("=" * 70)
        weather_forecast = self.weather_api.get_forecast(destination, days)
        plan['weather'] = weather_forecast
        print(f"✓ Weather forecast retrieved for {days} days")
        
        # Step 2: Get hotel recommendations
        print("\n" + "=" * 70)
        print("STEP 2: Hotel Recommendations")
        print("=" * 70)
        hotels = self._get_hotel_recommendations(destination, preferences.get('hotel_amenities', []))
        plan['hotels'] = hotels
        print(f"✓ Found {len(hotels)} hotel recommendations")
        
        # Step 3: Get attraction recommendations
        print("\n" + "=" * 70)
        print("STEP 3: Attraction Recommendations")
        print("=" * 70)
        attractions = self._get_attraction_recommendations(
            destination, budget.get('attractions', 500), 
            preferences.get('attraction_categories', {}), days
        )
        plan['attractions'] = attractions
        print(f"✓ Generated attraction recommendations")
        
        # Step 4: Get restaurant recommendations
        print("\n" + "=" * 70)
        print("STEP 4: Restaurant Recommendations")
        print("=" * 70)
        restaurants = self._get_restaurant_recommendations(
            destination, days, budget.get('food', 100),
            preferences.get('cuisine_preferences', [])
        )
        plan['restaurants'] = restaurants
        print(f"✓ Generated restaurant recommendations")
        
        # Step 5: Create daily itinerary with route optimization
        print("\n" + "=" * 70)
        print("STEP 5: Creating Daily Itinerary with Route Optimization")
        print("=" * 70)
        itinerary = self._create_daily_itinerary(plan, weather_forecast)
        plan['daily_itinerary'] = itinerary
        
        # Step 6: Optimize routes
        print("\n" + "=" * 70)
        print("STEP 6: Route Optimization")
        print("=" * 70)
        optimized_routes = self._optimize_routes(plan)
        plan['route_optimization'] = optimized_routes
        
        return plan
    
    def _get_hotel_recommendations(self, destination: str, amenities: List[str]) -> List[Dict]:
        """Get hotel recommendations"""
        if not self.spark:
            if not self.initialize_spark():
                return []
        
        try:
            try:
                from hotel_recc import amenities_rating, model_train, get_hotel_recc
            except ImportError:
                print("⚠️  Hotel recommendation module not available")
                return []
            
            from pyspark.sql import functions
            
            del_dup = self.spark.read.json('etl/del_dup')
            newh_df = self.spark.read.json('etl/newh_df')
            
            # Create temp views needed by amenities_rating
            del_dup.createOrReplaceTempView('del_dup')
            newh_df.createOrReplaceTempView('newh_df')
            
            if not amenities:
                amenities = ["Nonsmoking hotel", "Family Rooms", "Public Wifi", 
                           "Air conditioning", "Free parking"]
            
            try:
                usr_rating = amenities_rating(self.spark, amenities, newh_df)
                rank, error, errors, usrid_s2 = model_train(self.spark, usr_rating)
                u_tempdf = get_hotel_recc(self.spark, usrid_s2)
                
                hotel_df = del_dup.join(u_tempdf, "id").withColumn("address", 
                    functions.lower(functions.col("address")))
                hotel_sugg = hotel_df.where(hotel_df.address.contains(destination.lower()))
                recc = hotel_sugg.dropna().toPandas()
            except Exception as e:
                print(f"⚠️  Model-based recommendation failed: {e}")
                recc = pd.DataFrame()  # Empty dataframe
            
            if len(recc) == 0:
                # Fallback to direct search - this should work for Quebec!
                print(f"   Trying direct search for '{destination}'...")
                all_hotels = del_dup.withColumn("address", 
                    functions.lower(functions.col("address")))
                direct_hotels = all_hotels.where(all_hotels.address.contains(destination.lower()))
                recc = direct_hotels.dropna().toPandas()
                print(f"   Found {len(recc)} hotels in direct search")
                if len(recc) > 0 and 'hotel_rating' in recc.columns:
                    recc = recc.sort_values('hotel_rating', ascending=False)
                elif len(recc) > 0 and 'rating' in recc.columns:
                    recc = recc.sort_values('rating', ascending=False)
            
            hotels = []
            max_hotels = min(5, len(recc))
            for _, row in recc.head(max_hotels).iterrows():
                # Get location coordinates
                location = row.get('location', [0, 0])
                if isinstance(location, str):
                    try:
                        location = eval(location)
                    except:
                        location = [0, 0]
                
                hotels.append({
                    'name': row.get('hotel_name', 'Hotel'),
                    'price': float(row.get('price', 0)),
                    'rating': float(row.get('hotel_rating', 0)),
                    'address': row.get('address', ''),
                    'amenities': row.get('amenities', []),
                    'latitude': float(location[0]) if len(location) > 0 else 0,
                    'longitude': float(location[1]) if len(location) > 1 else 0
                })
            
            return hotels
        except Exception as e:
            print(f"⚠️  Hotel recommendation error: {e}")
            return []
    
    def _get_attraction_recommendations(self, destination: str, budget: float,
                                       categories: Dict, days: int) -> Dict:
        """Get attraction recommendations"""
        # Use module-level imports
        if not ATTRACTION_MODULE_AVAILABLE or _module_get_recc is None or _module_filter_df is None:
            print("⚠️  Attraction recommendations not available")
            return {}
        
        # Assign to local variables to ensure they're in scope
        get_recc_func = _module_get_recc
        filter_df_func = _module_filter_df
        
        # Double-check
        if get_recc_func is None or filter_df_func is None:
            print("⚠️  Functions are None")
            return {}
        
        try:
            att_df = pd.read_json('etl/attractions.json', orient='records')
            
            if not categories:
                categories = {
                    'tours_&_sightseeing': 4.0,
                    'outdoor_activities': 5.0,
                    'cultural_&_theme_tours': 4.0
                }
            
            # Convert destination to province format - try multiple variations
            province_variations = [
                destination.lower().replace(' ', '_'),
                destination.lower(),
                destination.lower().replace('_', ' ')
            ]
            
            # Try to get recommendations
            filename, user, rbm_att = get_recc_func(att_df, categories)
            
            # Try each province variation
            with_url = None
            for province in province_variations:
                try:
                    with_url = filter_df_func(filename, user, 0, budget, province, att_df)
                    if len(with_url) > 0:
                        print(f"   Found {len(with_url)} attractions for '{province}'")
                        break
                except:
                    continue
            
            if with_url is None or len(with_url) == 0:
                print(f"   No attractions found for '{destination}', trying broader search...")
                # Try without province filter
                try:
                    # Get top attractions regardless of location
                    recc_df = pd.read_csv(f'recommendations/{filename}/user{user}_unseen.csv', index_col=0)
                    recc_df.columns = ['attraction_id', 'att_name', 'att_cat', 'att_price', 'score']
                    recommendation = att_df[['attraction_id','name','category','city','latitude','longitude','price','province', 'rating']].set_index('attraction_id').join(recc_df[['attraction_id','score']].set_index('attraction_id'), how="inner").reset_index().sort_values("score",ascending=False)
                    with_url = recommendation.head(20)  # Get top 20
                    print(f"   Found {len(with_url)} attractions (no location filter)")
                except Exception as e:
                    print(f"   Could not get attractions: {e}")
                    return {}
            
            if len(with_url) == 0:
                return {}
            
            # Generate recommendations for each day
            attractions_by_day = {}
            attractions_list = []
            
            # Convert to list format for easier access
            for idx, row in with_url.iterrows():
                if len(attractions_list) >= days * 4:  # 2 morning + 2 evening per day
                    break
                attractions_list.append({
                    'name': row.get('name', 'Attraction'),
                    'latitude': row.get('latitude', 0),
                    'longitude': row.get('longitude', 0),
                    'price': row.get('price', 0),
                    'rating': row.get('rating', 0),
                    'category': row.get('category', ''),
                    'day': (len(attractions_list) // 4) + 1,
                    'time': 'morning' if (len(attractions_list) % 4) < 2 else 'evening'
                })
            
            # Organize by day
            for day in range(1, days + 1):
                day_attractions = {
                    'morning': [a for a in attractions_list if a.get('day') == day and a.get('time') == 'morning'],
                    'evening': [a for a in attractions_list if a.get('day') == day and a.get('time') == 'evening']
                }
                attractions_by_day[f'Day {day}'] = day_attractions
            
            return attractions_by_day
            
        except NameError as e:
            print(f"⚠️  NameError in _get_attraction_recommendations: {e}")
            import traceback
            traceback.print_exc()
            return {}
        except Exception as e:
            print(f"⚠️  Attraction recommendation error: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _get_restaurant_recommendations(self, destination: str, days: int,
                                       daily_budget: float, cuisine_prefs: List[str]) -> Dict:
        """Get restaurant recommendations"""
        self.restaurant_recommender.load_data()
        self.restaurant_recommender.train_models()
        
        return self.restaurant_recommender.recommend_for_trip(
            destination, days, daily_budget, cuisine_prefs
        )
    
    def _create_daily_itinerary(self, plan: Dict, weather: List[Dict]) -> Dict:
        """Create day-by-day itinerary considering weather"""
        itinerary = {}
        
        # Parse start_date if it's a string
        start_date = plan.get('start_date')
        if isinstance(start_date, str):
            from datetime import datetime
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        elif not isinstance(start_date, datetime.date):
            # Fallback to today
            start_date = datetime.now().date()
        
        for day in range(1, plan['days'] + 1):
            day_weather = weather[day - 1] if day - 1 < len(weather) else weather[0]
            
            itinerary[f'Day {day}'] = {
                'date': str(start_date + timedelta(days=day-1)),
                'weather': day_weather,
                'activities': [],
                'restaurants': plan['restaurants'].get(f'Day {day}', {}),
                'notes': []
            }
            
            # Add weather-based recommendations
            if self.weather_api.is_good_weather_for_activity(day_weather, 'outdoor'):
                itinerary[f'Day {day}']['notes'].append('Great weather for outdoor activities!')
            else:
                itinerary[f'Day {day}']['notes'].append('Consider indoor activities due to weather')
        
        return itinerary
    
    def _optimize_routes(self, plan: Dict) -> Dict:
        """Optimize routes for each day"""
        optimized = {}
        
        for day in range(1, plan['days'] + 1):
            day_key = f'Day {day}'
            locations = []
            
            # Collect all locations for the day
            # (Attractions, restaurants, hotels)
            # Then optimize route
            
            if locations:
                optimized_route, total_distance = optimize_route(locations)
                optimized[day_key] = {
                    'route': optimized_route,
                    'total_distance_km': total_distance,
                    'estimated_time_minutes': calculate_travel_time(total_distance)
                }
        
        return optimized
    
    def display_plan(self, plan: Dict):
        """Display the complete travel plan"""
        print("\n" + "=" * 70)
        print("📋 COMPLETE TRAVEL PLAN")
        print("=" * 70)
        
        print(f"\n👤 Traveler: {plan['user_name']}")
        print(f"📍 Destination: {plan['destination'].title()}")
        print(f"📅 Dates: {plan['start_date']} to {plan['end_date']}")
        print(f"💰 Total Budget: ${plan['budget'].get('total', 0):.2f}")
        
        # Weather summary
        print(f"\n🌤️  Weather Forecast:")
        for day_weather in plan['weather'][:3]:
            print(f"   {day_weather.get('date', 'N/A')}: {day_weather.get('temperature', 0)}°C, "
                  f"{day_weather.get('description', 'N/A')}")
        
        # Hotels
        print(f"\n🏨 Hotel Recommendations ({len(plan['hotels'])}):")
        for i, hotel in enumerate(plan['hotels'][:3], 1):
            print(f"   {i}. {hotel.get('name', 'Hotel')} - ${hotel.get('price', 0):.2f}/night, "
                  f"⭐ {hotel.get('rating', 0)}/5.0")
        
        # Daily itinerary
        print(f"\n📅 Daily Itinerary:")
        for day_key, day_plan in plan['daily_itinerary'].items():
            print(f"\n   {day_key} - {day_plan.get('date', 'N/A')}")
            print(f"      Weather: {day_plan.get('weather', {}).get('description', 'N/A')}")
            if day_plan.get('notes'):
                for note in day_plan['notes']:
                    print(f"      💡 {note}")

