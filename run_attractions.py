#!/usr/bin/env python3
"""
Script to run attraction recommendations without Jupyter widgets
"""
import pandas as pd
import re
from datetime import datetime, timedelta
from attractions_recc import get_recc, filter_df, top_recc, find_closest, final_output
import sys

def get_user_inputs():
    """Get user inputs for recommendations"""
    print("=" * 60)
    print("ATTRACTION RECOMMENDATION SYSTEM")
    print("=" * 60)
    
    # User name
    user_name = input("\nEnter your name: ").strip()
    if not user_name:
        user_name = "User"
    
    # Destination/Province
    print("\nEnter destination province (e.g., Ontario, British Columbia, Quebec):")
    province = input("Province: ").strip()
    if not province:
        province = "Ontario"
    
    # Budget
    print("\nBudget range (min: 5, max: 999):")
    try:
        budget_min = float(input("Minimum budget ($): ").strip() or "5")
        budget_max = float(input("Maximum budget ($): ").strip() or "999")
        budget_min = max(5, min(999, budget_min))
        budget_max = max(budget_min, min(999, budget_max))
    except:
        budget_min, budget_max = 5.0, 999.0
    
    # Dates
    print("\nEnter trip dates:")
    try:
        start_str = input("Start date (YYYY-MM-DD) or press Enter for today: ").strip()
        if start_str:
            begin_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        else:
            begin_date = datetime.now().date()
        
        end_str = input("End date (YYYY-MM-DD) or press Enter for tomorrow: ").strip()
        if end_str:
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        else:
            end_date = begin_date + timedelta(days=1)
        
        if end_date < begin_date:
            end_date = begin_date + timedelta(days=1)
    except:
        begin_date = datetime.now().date()
        end_date = begin_date + timedelta(days=1)
    
    # Categories
    print("\n" + "=" * 60)
    print("CATEGORY SELECTION")
    print("=" * 60)
    print("\nAvailable categories:")
    
    att_df = pd.read_json('etl/attractions.json', orient='records')
    category_df = att_df.groupby('category').size().reset_index().sort_values([0], ascending=False)[:20]
    categories = list(category_df.category.values)
    
    for i, cat in enumerate(categories, 1):
        print(f"{i:2d}. {cat}")
    
    print("\nSelect and rate at least 5 categories (rate 0-5):")
    cat_rating = {}
    
    while len(cat_rating) < 5:
        try:
            choice = input(f"\nSelect category number (1-{len(categories)}) or category name: ").strip()
            
            # Try to parse as number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    selected_cat = categories[idx]
                else:
                    print("Invalid number. Please try again.")
                    continue
            else:
                # Try to find by name
                selected_cat = None
                for cat in categories:
                    if choice.lower() in cat.lower() or cat.lower() in choice.lower():
                        selected_cat = cat
                        break
                
                if not selected_cat:
                    print("Category not found. Please try again.")
                    continue
            
            if selected_cat in cat_rating:
                print(f"You already rated '{selected_cat}'. Choose another.")
                continue
            
            rating = input(f"Rate '{selected_cat}' (0-5): ").strip()
            try:
                rating_val = float(rating)
                if 0 <= rating_val <= 5:
                    cat_rating[selected_cat] = rating_val
                    print(f"✓ Rated '{selected_cat}' as {rating_val}")
                    remaining = 5 - len(cat_rating)
                    if remaining > 0:
                        print(f"  ({remaining} more categories needed)")
                else:
                    print("Rating must be between 0 and 5.")
            except:
                print("Invalid rating. Please enter a number between 0 and 5.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}. Please try again.")
    
    print(f"\n✓ Selected {len(cat_rating)} categories:")
    for cat, rating in cat_rating.items():
        print(f"  - {cat}: {rating}")
    
    return {
        'user_name': user_name,
        'province': province,
        'budget_min': budget_min,
        'budget_max': budget_max,
        'begin_date': begin_date,
        'end_date': end_date,
        'cat_rating': cat_rating,
        'att_df': att_df
    }

def main():
    """Main execution function"""
    try:
        # Get user inputs
        inputs = get_user_inputs()
        
        print("\n" + "=" * 60)
        print("GENERATING RECOMMENDATIONS...")
        print("=" * 60)
        
        # Get recommendations
        filename, user, rbm_att = get_recc(inputs['att_df'], inputs['cat_rating'])
        
        # Filter results
        with_url = filter_df(filename, user, inputs['budget_min'], inputs['budget_max'], 
                           inputs['province'], inputs['att_df'])
        
        print(f"\n✓ Found {len(with_url)} matching attractions")
        
        # Generate final recommendations
        print("\nGenerating daily recommendations...")
        final = {
            'timeofday': [],
            'image': [],
            'name': [],
            'location': [],
            'price': [],
            'rating': [],
            'category': []
        }
        
        days = (inputs['end_date'] - inputs['begin_date']).days + 1
        total_recommendations = days * 4  # 2 morning + 2 evening per day
        
        for i in range(days):
            for j in range(2):
                final['timeofday'].append('Morning')
            for j in range(2):
                final['timeofday'].append('Evening')
        
        for i in range(len(final['timeofday'])):
            if i % 4 == 0:
                final = top_recc(with_url, final)
            else:
                if len(final['location']) > 0:
                    final = find_closest(with_url, final['location'][-1], final['timeofday'][i], final)
        
        # Display results
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS GENERATED!")
        print("=" * 60)
        print(f"\nTrip Duration: {days} day(s)")
        print(f"Total Recommendations: {len(final['name'])}")
        print(f"\nRecommendations by Day:")
        
        for day in range(days):
            print(f"\n--- Day {day + 1} ---")
            start_idx = day * 4
            for i in range(4):
                idx = start_idx + i
                if idx < len(final['name']):
                    time = final['timeofday'][idx]
                    name = final['name'][idx]
                    cat = final['category'][idx]
                    price = final['price'][idx]
                    rating = final['rating'][idx]
                    loc = final['location'][idx]
                    print(f"\n{time} - Recommendation {i % 2 + 1}:")
                    print(f"  Name: {name}")
                    print(f"  Category: {cat}")
                    print(f"  Price: ${price}")
                    print(f"  Rating: {rating}")
                    print(f"  Location: ({loc[0]:.4f}, {loc[1]:.4f})")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Recommendations complete.")
        print("=" * 60)
        print("\nNote: For visual display with images, run the notebook in Jupyter.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

