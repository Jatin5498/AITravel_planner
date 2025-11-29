# 🏨 Hotel Recommendations - Running Guide

## ⚠️ Current Issue

The hotel recommendation system uses **PySpark** which requires **Java 8 or 11**. Your system has Java 25, which has compatibility issues with PySpark.

## ✅ Solutions

### Option 1: Use Jupyter Notebook (Recommended)
The notebook version works better with Java compatibility:

```bash
# 1. Make sure Jupyter is running
jupyter notebook

# 2. Open final_hotel_recc.ipynb
# 3. Run all cells
# 4. Fill in the interactive form:
#    - User Name
#    - Destination (e.g., "toronto", "vancouver")
#    - Start Date and End Date
#    - Select at least 5 amenities (click buttons)
```

### Option 2: Install Java 11
```bash
# Install Java 11
brew install openjdk@11

# Set JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 11)

# Then run the script
python3 run_hotels_sample.py
```

### Option 3: Use Pre-trained Model (Simplified)
The system can use the existing pre-trained model without retraining.

---

## 📋 How Hotel Recommendations Work

### Input Required:
1. **User Name** - Your name
2. **Destination** - City name (e.g., "toronto", "vancouver", "montreal")
3. **Dates** - Start and end date of trip
4. **Amenities** - Select at least 5 from:
   - Nonsmoking hotel
   - Family Rooms
   - Public Wifi
   - Pets Allowed
   - Air conditioning
   - Free parking
   - Pool
   - Gym/Fitness Center
   - Restaurant
   - Bar/Lounge
   - Room service
   - Business center
   - Spa
   - Concierge
   - Laundry service

### Process:
1. **Amenity Matching** - System finds hotels matching your selected amenities
2. **Rating Calculation** - Hotels are rated based on how many amenities match
3. **Model Training** - Matrix Factorization (ALS) model is trained/retrained
4. **Recommendations** - Top 5 hotels are recommended
5. **Location Filtering** - Hotels are filtered by destination city

### Output:
- Top 5 hotel recommendations with:
  - Hotel name
  - Price
  - Rating
  - Experience level
  - Location (coordinates)
  - Address
  - Amenities list
  - Images

---

## 🎯 Sample Inputs

```python
user_name = "Pranav Mittal"
destination = "toronto"  # lowercase city name
start_date = "2025-11-12"
end_date = "2025-11-15"

amenities = [
    "Nonsmoking hotel",
    "Family Rooms", 
    "Public Wifi",
    "Air conditioning",
    "Free parking"
]
```

---

## 📊 Available Destinations

The hotel dataset contains hotels from various cities. Common destinations include:
- toronto
- vancouver
- montreal
- calgary
- ottawa
- edmonton
- And many more...

---

## 🔧 Technical Details

**Algorithm:** Matrix Factorization with ALS (Alternating Least Squares)
- Collaborative filtering approach
- Learns latent factors from user-hotel interactions
- Handles cold-start problem for new users

**Model Parameters:**
- Ranks tested: [4, 8, 12]
- Best rank selected based on RMSE
- Model saved in `mf_models/model_file/`

---

## 💡 Tips

1. **Select diverse amenities** - More variety = better matching
2. **Use specific city names** - Better filtering results
3. **Check available amenities** - Not all hotels have all amenities
4. **For best results** - Use Jupyter notebook for interactive experience

---

## 🚀 Quick Start (Jupyter)

1. Open Jupyter: `jupyter notebook`
2. Navigate to `final_hotel_recc.ipynb`
3. Run all cells
4. Fill in the form when prompted
5. Get your top 5 hotel recommendations!

---

**Note:** The script version (`run_hotels_sample.py`) requires Java 11. For now, use the Jupyter notebook version which handles Java compatibility better.

