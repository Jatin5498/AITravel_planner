#!/usr/bin/env python3
"""
Quick script to run complete travel plan with sample data
"""
from travel_planner import TravelPlanner
from datetime import date, timedelta

def main():
    """Run complete travel plan with sample inputs"""
    print("=" * 70)
    print("🌍 AI-BASED TRAVEL RECOMMENDATION SYSTEM")
    print("Complete Travel Plan Generator")
    print("=" * 70)
    
    # Sample inputs
    user_name = "Pranav Mittal"
    destination = "vancouver"
    start_date = date.today()
    end_date = start_date + timedelta(days=3)
    
    budget = {
        'total': 1500.0,
        'hotel': 600.0,
        'attractions': 400.0,
        'food': 500.0
    }
    
    preferences = {
        'attraction_categories': {
            'tours_&_sightseeing': 4.0,
            'outdoor_activities': 5.0,
            'cultural_&_theme_tours': 4.0,
            'food,_wine_&_nightlife': 3.0,
            'walking_&_biking_tours': 4.0
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
    
    print(f"\n📋 Sample Inputs:")
    print(f"  Name: {user_name}")
    print(f"  Destination: {destination.title()}")
    print(f"  Dates: {start_date} to {end_date}")
    print(f"  Budget: ${budget['total']:.2f}")
    
    # Initialize planner
    planner = TravelPlanner()
    
    # Create plan
    plan = planner.create_travel_plan(
        user_name=user_name,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        preferences=preferences
    )
    
    # Display plan
    planner.display_plan(plan)
    
    print("\n" + "=" * 70)
    print("✅ Complete travel plan generated!")
    print("=" * 70)

if __name__ == "__main__":
    main()

