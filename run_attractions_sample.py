#!/usr/bin/env python3
"""
Script to run attraction recommendations with sample inputs
"""
import pandas as pd
import re
from datetime import datetime, timedelta
from attractions_recc import get_recc, filter_df, top_recc, find_closest, final_output
import sys

def main():
    """Main execution function with sample inputs"""
    try:
        print("=" * 60)
        print("ATTRACTION RECOMMENDATION SYSTEM")
        print("Running with SAMPLE INPUTS")
        print("=" * 60)
        
        # Sample inputs
        user_name = "Pranav Mittal"
        # NOTE: India has only 1 attraction, and it's NOT in RBM recommendations
        # Best options with most attractions:
        #   - "british_columbia" (1,346 attractions) - BEST
        #   - "ontario" (688 attractions) - GOOD
        #   - "quebec" (497 attractions) - GOOD
        #   - "italy" (39 attractions) - International option
        province = "alberta"  # Must be lowercase with underscores
        budget_min = 50.0
        budget_max = 50000.0
        begin_date = datetime.now().date()
        end_date = begin_date + timedelta(days=5)  # 3-day trip
        
        # Sample category ratings (at least 5)
        cat_rating = {
            'tours_&_sightseeing': 4.0,
            'outdoor_activities': 5.0,
            'cultural_&_theme_tours': 4.0,
            'food,_wine_&_nightlife': 3.0,
            'walking_&_biking_tours': 4.0
        }
        
        print(f"\nSample Inputs:")
        print(f"  Name: {user_name}")
        print(f"  Province: {province}")
        print(f"  Budget: ${budget_min} - ${budget_max}")
        print(f"  Dates: {begin_date} to {end_date}")
        print(f"  Categories rated: {len(cat_rating)}")
        for cat, rating in cat_rating.items():
            print(f"    - {cat}: {rating}")
        
        # Load attractions data
        print("\nLoading attractions data...")
        att_df = pd.read_json('etl/attractions.json', orient='records')
        print(f"✓ Loaded {len(att_df)} attractions")
        
        print("\n" + "=" * 60)
        print("GENERATING RECOMMENDATIONS...")
        print("=" * 60)
        
        # Get recommendations
        print("\nStep 1: Finding similar user and loading RBM model...")
        filename, user, rbm_att = get_recc(att_df, cat_rating)
        
        # Filter results
        print("\nStep 2: Filtering attractions by budget and province...")
        with_url = filter_df(filename, user, budget_min, budget_max, province, att_df)
        
        print(f"\n✓ Found {len(with_url)} matching attractions")
        
        if len(with_url) == 0:
            print("\n⚠️  No attractions found matching the criteria.")
            print("   Try adjusting budget range or province.")
            return
        
        # Generate final recommendations
        print("\nStep 3: Generating daily recommendations...")
        final = {
            'timeofday': [],
            'image': [],
            'name': [],
            'location': [],
            'price': [],
            'rating': [],
            'category': []
        }
        
        days = (end_date - begin_date).days + 1
        total_recommendations = days * 4  # 2 morning + 2 evening per day
        
        # Create time of day list
        for i in range(days):
            for j in range(2):
                final['timeofday'].append('Morning')
            for j in range(2):
                final['timeofday'].append('Evening')
        
        # Generate recommendations
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
        print(f"\n{'='*60}")
        print("RECOMMENDATIONS BY DAY")
        print(f"{'='*60}")
        
        for day in range(days):
            print(f"\n{'─'*60}")
            print(f"DAY {day + 1} - {begin_date + timedelta(days=day)}")
            print(f"{'─'*60}")
            start_idx = day * 4
            for i in range(4):
                idx = start_idx + i
                if idx < len(final['name']):
                    time = final['timeofday'][idx]
                    rec_num = (i % 2) + 1
                    name = final['name'][idx]
                    cat = final['category'][idx]
                    price = final['price'][idx]
                    rating = final['rating'][idx]
                    loc = final['location'][idx]
                    
                    print(f"\n{time} - Recommendation {rec_num}:")
                    print(f"  📍 Name: {name}")
                    print(f"  🏷️  Category: {cat}")
                    print(f"  💰 Price: ${price:.2f}")
                    print(f"  ⭐ Rating: {rating:.1f}/5.0")
                    print(f"  📌 Location: ({loc[0]:.4f}, {loc[1]:.4f})")
        
        print(f"\n{'='*60}")
        print("SUCCESS! Recommendations complete.")
        print(f"{'='*60}")
        print("\nNote: For visual display with images, run the notebook in Jupyter.")
        print(f"Model used: {filename}")
        print(f"Similar user ID: {user}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

