#!/usr/bin/env python3
"""
Script to run hotel recommendations with sample inputs
"""
import pandas as pd
from datetime import datetime, timedelta
from hotel_recc import amenities_rating, model_train, get_hotel_recc, get_image
import pyspark
from pyspark.sql import SQLContext, functions, types
import sys
import os

def get_top_amenities(spark, newh_df):
    """Get top amenities from the dataset"""
    newh_df.createOrReplaceTempView('newh_df')
    newh1_df = spark.sql("SELECT amenities,COUNT(amenities) AS tot_count FROM newh_df GROUP BY amenities ORDER BY tot_count DESC")
    top_amenities = [x[0] for x in newh1_df.head(16) if x[0] != '']
    return top_amenities

def main():
    """Main execution function with sample inputs"""
    try:
        print("=" * 60)
        print("HOTEL RECOMMENDATION SYSTEM")
        print("Running with SAMPLE INPUTS")
        print("=" * 60)
        
        # Sample inputs
        user_name = "Pranav Mittal"
        # Available cities: quebec (752), saskatoon (54), charlottetown (50), halifax (46), 
        # st. john (47), vancouver (27), victoria (29), banff (21), etc.
        # See CITIES_GUIDE.md for complete list
        destination = "saskatoon"  # Best coverage - 752 hotels!
        begin_date = datetime.now().date()
        end_date = begin_date + timedelta(days=7)  # 4-day trip
        
        # Sample amenities (select at least 5)
        # These are common amenities - you can modify this list
        amenities_pref = [
            "Nonsmoking hotel",
            "Family Rooms",
            "Public Wifi",
            "Air conditioning",
            "Free parking"
        ]
        
        print(f"\nSample Inputs:")
        print(f"  Name: {user_name}")
        print(f"  Destination: {destination}")
        print(f"  Dates: {begin_date} to {end_date}")
        print(f"  Selected Amenities ({len(amenities_pref)}):")
        for amenity in amenities_pref:
            print(f"    - {amenity}")
        
        # Set Java 17 for PySpark (PySpark 4.0.1 requires Java 17+)
        import os
        java17_home = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
        if os.path.exists(java17_home):
            os.environ['JAVA_HOME'] = java17_home
            os.environ['PATH'] = f"{java17_home}/bin:{os.environ.get('PATH', '')}"
            print(f"\n✓ Java 17 configured: {java17_home}")
        else:
            # Try alternative method
            import subprocess
            try:
                java17_alt = subprocess.check_output(['/usr/libexec/java_home', '-v', '17'], 
                                                     stderr=subprocess.DEVNULL).decode().strip()
                if java17_alt:
                    os.environ['JAVA_HOME'] = java17_alt
                    os.environ['PATH'] = f"{java17_alt}/bin:{os.environ.get('PATH', '')}"
                    print(f"\n✓ Java 17 configured: {java17_alt}")
            except:
                print("\n⚠️  Java 17 not found. Trying system Java...")
        
        # Initialize PySpark
        print("\n" + "=" * 60)
        print("INITIALIZING PYSPARK...")
        print("=" * 60)
        
        try:
            sc = pyspark.SparkContext(appName="hotel_recc")
            spark = SQLContext(sc)
            print("✓ PySpark initialized successfully")
        except Exception as e:
            print(f"\n⚠️  PySpark initialization failed: {e}")
            print("\nTo fix this:")
            print("1. Install Java 11: brew install openjdk@11")
            print("2. Run: source setup_java11.sh")
            print("3. Or use the Jupyter notebook: final_hotel_recc.ipynb")
            raise
        
        # Load hotel data
        print("\nLoading hotel data...")
        del_dup = spark.read.json('etl/del_dup')
        newh_df = spark.read.json('etl/newh_df')
        
        del_dup.createOrReplaceTempView('del_dup')
        newh_df.createOrReplaceTempView('newh_df')
        
        print(f"✓ Loaded hotel data")
        
        # Get top amenities (for reference)
        top_amenities = get_top_amenities(spark, newh_df)
        print(f"\nTop amenities available: {len(top_amenities)}")
        print(f"Sample: {top_amenities[:5]}")
        
        print("\n" + "=" * 60)
        print("GENERATING RECOMMENDATIONS...")
        print("=" * 60)
        
        # Step 1: Rate hotels based on amenities
        print("\nStep 1: Rating hotels based on selected amenities...")
        usr_rating = amenities_rating(spark, amenities_pref, newh_df)
        print(f"✓ Rated hotels based on amenities")
        
        # Step 2: Train/retrain model
        print("\nStep 2: Training Matrix Factorization model...")
        print("  (This may take a few minutes...)")
        rank, error, errors, usrid_s2 = model_train(spark, usr_rating)
        print(f"✓ Model trained")
        print(f"  Best rank: {rank}")
        print(f"  Best RMSE: {error:.4f}")
        
        # Step 3: Get recommendations
        print("\nStep 3: Getting hotel recommendations...")
        u_tempdf = get_hotel_recc(spark, usrid_s2)
        
        # Filter by destination
        hotel_df = del_dup.join(u_tempdf, "id").withColumn("address", functions.lower(functions.col("address")))
        user_location = destination.lower()
        hotel_sugg = hotel_df.where(hotel_df.address.contains(user_location))
        recc = hotel_sugg.dropna().toPandas()
        
        print(f"✓ Found {len(recc)} hotels matching destination '{destination}' in recommendations")
        
        # If no hotels found in recommendations, try direct search from all hotels
        if len(recc) == 0:
            print(f"\n⚠️  No recommended hotels found for '{destination}'")
            print(f"   Trying direct search from all hotels in '{destination}'...")
            
            # Direct search from all hotels (not just recommendations)
            all_hotels = del_dup.withColumn("address", functions.lower(functions.col("address")))
            direct_hotels = all_hotels.where(all_hotels.address.contains(user_location))
            recc = direct_hotels.dropna().toPandas()
            
            if len(recc) > 0:
                print(f"✓ Found {len(recc)} hotels directly in '{destination}'")
                # Sort by rating for better results
                if 'hotel_rating' in recc.columns:
                    recc = recc.sort_values('hotel_rating', ascending=False)
            else:
                print(f"\n⚠️  No hotels found for destination '{destination}'")
                print("   Available cities: quebec, saskatoon, vancouver, halifax, charlottetown, etc.")
                print("   See CITIES_GUIDE.md for complete list")
                sc.stop()
                return
        
        # Prepare final recommendations (top 5)
        print("\nStep 4: Preparing final recommendations...")
        final = {
            'address': recc[:5]['address'].values.tolist(),
            'amenities': recc[:5]['amenities'].values.T.tolist(),
            'experience': recc[:5]['hotel_experience'].values.tolist(),
            'name': recc[:5]['hotel_name'].values.tolist(),
            'rating': recc[:5]['hotel_rating'].values.tolist(),
            'location': [i[1:-1] if isinstance(i, str) else str(i) for i in recc[:5]['location'].values.tolist()],
            'price': recc[:5]['price'].values.tolist(),
            'image': []
        }
        
        # Download images (this may take time)
        print("  Downloading hotel images...")
        for i, name in enumerate(final['name'][:5]):
            print(f"    {i+1}/5: {name}")
            try:
                img_path = get_image(name)
                final['image'].append(img_path)
            except:
                # Use default image if download fails
                final['image'].append("downloads/noimage.jpg")
        
        # Display results
        print("\n" + "=" * 60)
        print("HOTEL RECOMMENDATIONS")
        print("=" * 60)
        print(f"\nTrip Duration: {(end_date - begin_date).days + 1} day(s)")
        print(f"Destination: {destination.title()}")
        print(f"Total Recommendations: {len(final['name'])}")
        print(f"\n{'='*60}")
        print("TOP 5 HOTEL RECOMMENDATIONS")
        print(f"{'='*60}")
        
        for i in range(len(final['name'])):
            print(f"\n{'─'*60}")
            print(f"HOTEL {i+1}")
            print(f"{'─'*60}")
            print(f"🏨 Name: {final['name'][i]}")
            print(f"💰 Price: ${final['price'][i]}")
            print(f"⭐ Rating: {final['rating'][i]}/5.0")
            print(f"📝 Experience: {final['experience'][i]}")
            print(f"📍 Location: {final['location'][i]}")
            print(f"🏠 Address: {final['address'][i]}")
            if isinstance(final['amenities'][i], list):
                amenities_str = ", ".join(final['amenities'][i][:5])  # Show first 5
                print(f"✨ Amenities: {amenities_str}")
            else:
                print(f"✨ Amenities: {final['amenities'][i]}")
        
        print(f"\n{'='*60}")
        print("SUCCESS! Hotel recommendations complete.")
        print(f"{'='*60}")
        print("\nNote: For visual display with images, run the notebook in Jupyter.")
        
        sc.stop()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

