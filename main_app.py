#!/usr/bin/env python3
"""
Main Application - AI-Based Travel Recommendation System
Unified interface for complete travel planning
"""
import sys
from datetime import datetime, timedelta
from travel_planner import TravelPlanner
import json

def get_user_preferences():
    """Interactive function to get user preferences"""
    print("=" * 70)
    print("🌍 AI-BASED TRAVEL RECOMMENDATION SYSTEM")
    print("=" * 70)
    print("\nLet's create your personalized travel plan!\n")
    
    # Basic information
    user_name = input("Your name: ").strip() or "Traveler"
    destination = input("Destination city: ").strip() or "vancouver"
    
    # Dates
    print("\nTrip dates:")
    start_str = input("Start date (YYYY-MM-DD) or press Enter for today: ").strip()
    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except:
            start_date = datetime.now().date()
    else:
        start_date = datetime.now().date()
    
    end_str = input("End date (YYYY-MM-DD) or press Enter for tomorrow: ").strip()
    if end_str:
        try:
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        except:
            end_date = start_date + timedelta(days=1)
    else:
        end_date = start_date + timedelta(days=1)
    
    # Budget
    print("\nBudget:")
    try:
        total_budget = float(input("Total budget ($): ").strip() or "1000")
        hotel_budget = float(input("Hotel budget per night ($): ").strip() or str(total_budget * 0.4))
        attraction_budget = float(input("Attractions budget ($): ").strip() or str(total_budget * 0.3))
        food_budget = float(input("Food budget per day ($): ").strip() or str(total_budget * 0.3))
    except:
        total_budget = 1000
        hotel_budget = 400
        attraction_budget = 300
        food_budget = 300
    
    budget = {
        'total': total_budget,
        'hotel': hotel_budget,
        'attractions': attraction_budget,
        'food': food_budget
    }
    
    # Preferences
    print("\nPreferences:")
    print("Attraction categories (rate 0-5, press Enter to skip):")
    categories = {}
    cat_list = ['tours_&_sightseeing', 'outdoor_activities', 'cultural_&_theme_tours', 
                'food,_wine_&_nightlife', 'walking_&_biking_tours']
    
    for cat in cat_list[:3]:  # Get at least 3
        rating = input(f"  {cat} (0-5): ").strip()
        if rating:
            try:
                categories[cat] = float(rating)
            except:
                pass
    
    if not categories:
        categories = {'tours_&_sightseeing': 4.0, 'outdoor_activities': 5.0, 
                     'cultural_&_theme_tours': 4.0}
    
    hotel_amenities_input = input("\nHotel amenities (comma-separated, or press Enter for default): ").strip()
    if hotel_amenities_input:
        hotel_amenities = [a.strip() for a in hotel_amenities_input.split(',')]
    else:
        hotel_amenities = ["Nonsmoking hotel", "Family Rooms", "Public Wifi", 
                          "Air conditioning", "Free parking"]
    
    cuisine_input = input("Preferred cuisines (comma-separated, or press Enter for default): ").strip()
    if cuisine_input:
        cuisine_preferences = [c.strip() for c in cuisine_input.split(',')]
    else:
        cuisine_preferences = ['Local', 'Italian', 'Asian']
    
    preferences = {
        'attraction_categories': categories,
        'hotel_amenities': hotel_amenities,
        'cuisine_preferences': cuisine_preferences,
        'activity_interests': ['outdoor', 'cultural', 'food']
    }
    
    return {
        'user_name': user_name,
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
        'budget': budget,
        'preferences': preferences
    }

def main():
    """Main application entry point"""
    try:
        # Get user input
        user_input = get_user_preferences()
        
        # Initialize travel planner
        planner = TravelPlanner()
        
        # Create travel plan
        plan = planner.create_travel_plan(
            user_name=user_input['user_name'],
            destination=user_input['destination'],
            start_date=user_input['start_date'],
            end_date=user_input['end_date'],
            budget=user_input['budget'],
            preferences=user_input['preferences']
        )
        
        # Display plan
        planner.display_plan(plan)
        
        # Save plan to file
        plan_filename = f"travel_plan_{user_input['destination']}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(plan_filename, 'w') as f:
            # Convert dates to strings for JSON
            plan_json = json.loads(json.dumps(plan, default=str))
            json.dump(plan_json, f, indent=2)
        
        print(f"\n✅ Travel plan saved to: {plan_filename}")
        print("\n" + "=" * 70)
        print("🎉 Your personalized travel plan is ready!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Plan generation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

