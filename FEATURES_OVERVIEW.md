# 🎯 Intelligent Travel Recommendation System - Complete Features Overview

## 📋 Main Features

This project provides **3 major recommendation systems** for complete travel planning:

---

## 1. 🎪 **ATTRACTION RECOMMENDATIONS** (Currently Working ✅)

### Technology: RBM (Restricted Boltzmann Machine) - Deep Learning

**What it does:**
- Recommends attractions based on your category preferences
- Suggests **2 attractions per time slot** (Morning & Evening) for each day
- Considers timing - which attractions are better for day vs. night
- Filters by location, budget, and user preferences

**Features:**
- ✅ Personalized recommendations using deep learning
- ✅ Category-based filtering (tours, outdoor activities, cultural tours, etc.)
- ✅ Budget filtering ($5 - $999 range)
- ✅ Location-based recommendations (97+ locations available)
- ✅ Time-of-day recommendations (Morning/Evening)
- ✅ Distance-based clustering (recommends nearby attractions)
- ✅ Image downloads for attractions
- ✅ Rating and price information

**Files:**
- `get_att_recc.ipynb` - Main notebook
- `attractions_recc.py` - Core recommendation functions
- `rbm.py` - RBM model implementation
- `rbm_training.ipynb` - Model training notebook

**Status:** ✅ **Fully Working** - You just ran this!

---

## 2. 🏨 **HOTEL RECOMMENDATIONS** (Available)

### Technology: Matrix Factorization with ALS (Alternating Least Squares)

**What it does:**
- Recommends **5 top hotels** based on your amenity preferences
- Uses collaborative filtering to match your preferences
- Considers hotel amenities (WiFi, Pool, Parking, etc.)
- Provides hotel details: name, price, rating, location, address, amenities

**Features:**
- ✅ Amenity-based matching (select 5+ amenities you want)
- ✅ Collaborative filtering using Matrix Factorization
- ✅ Hotel rating and pricing information
- ✅ Location and address details
- ✅ Image downloads for hotels
- ✅ Personalized recommendations based on similar users

**How it works:**
1. You select 5+ hotel amenities (WiFi, Pool, Gym, etc.)
2. System finds hotels matching your preferences
3. Uses ALS model to rank hotels
4. Returns top 5 recommendations

**Files:**
- `final_hotel_recc.ipynb` - Main notebook
- `hotel_recc.py` - Core recommendation functions
- `hotel_etl.ipynb` - Data processing
- `mf_models/` - Pre-trained Matrix Factorization model

**Status:** ✅ **Available** - Ready to run (requires PySpark)

**To Run:**
```python
# Open final_hotel_recc.ipynb in Jupyter
# Run all cells
# Select amenities and get recommendations
```

---

## 3. 🍽️ **RESTAURANT RECOMMENDATIONS** (Requires Dataset)

### Technology: Hybrid Recommender (K-Means + K-Nearest Neighbors)

**What it does:**
- Recommends restaurants for **each meal** (Breakfast, Lunch, Dinner)
- Provides **2 recommendations per meal per day**
- Uses hybrid approach: Content-based + Collaborative filtering
- Considers cuisine type, price range, location, ratings

**Features:**
- ✅ Meal-specific recommendations (Breakfast/Lunch/Dinner)
- ✅ Hybrid recommendation system
- ✅ Content-based filtering (cuisine, price, location)
- ✅ Collaborative filtering (similar users)
- ✅ Multiple recommendations per meal

**Requirements:**
- ⚠️ Requires Yelp dataset (not included)
- Download from: https://www.yelp.ca/dataset/download
- Store in `yelp_dataset/` folder

**Files:**
- `Hybrid_Recommder.ipynb` - Main notebook (if available)
- `Restaurants (Yelp) Dataset-EDA.ipynb` - EDA visualizations

**Status:** ⚠️ **Requires Dataset** - Need to download Yelp data first

---

## 4. 📊 **DATA ANALYSIS & VISUALIZATION**

### EDA (Exploratory Data Analysis)

**Available Visualizations:**
- **Attractions (a1.png - a9.png):** 9 visualizations
  - Distribution of attractions
  - Category analysis
  - Price ranges
  - Location distributions
  - Rating analysis
  
- **Hotels (h1.png - h5.png):** 5 visualizations
  - Hotel amenities distribution
  - Price analysis
  - Rating distributions
  - Location patterns
  
- **Restaurants (r1.png - r8.png):** 8 visualizations
  - Cuisine types
  - Price ranges
  - Rating distributions
  - Location patterns

**Files:**
- `EDA/` folder - Contains all visualization images
- `Restaurants (Yelp) Dataset-EDA.ipynb` - Restaurant EDA code

---

## 5. 🕷️ **DATA SCRAPING & COLLECTION**

### Web Scraping Capabilities

**Attractions Scraping:**
- `attractions_crawler.ipynb` - Collects attraction URLs from TripAdvisor
- `attractions_details_crawler.ipynb` - Extracts attraction details and reviews
- `combine_batches.ipynb` - Combines scraped data from batches

**Hotel Scraping:**
- `TripAdvisor_Crawler_Parser.ipynb` - Scrapes hotel data from TripAdvisor
  - Hotel URLs
  - Hotel information
  - User reviews
  - User ratings
  - User profiles

**Features:**
- ✅ Batch processing
- ✅ Data cleaning and deduplication
- ✅ Review extraction
- ✅ Rating collection

---

## 6. 🔧 **MODEL TRAINING & TUNING**

### RBM Model Training

**Features:**
- Train custom RBM models with different parameters
- Hyperparameter tuning:
  - Epochs (10, 20, 50)
  - Hidden units (64, 128, 256)
  - Learning rate
  - Batch size
  - Number of rows
- Model evaluation and comparison
- Error plotting
- Free energy visualization

**Files:**
- `rbm_training.ipynb` - Training notebook
- `recommendations/` - Saved models with different configurations

**Pre-trained Models Available:**
- `e10_r5000_lr0.01_hu64_bs8`
- `e20_r20000_lr0.01_hu128_bs16`
- `e20_r20000_lr0.01_hu64_bs16`
- `e20_r40000_lr0.01_hu128_bs8`
- `e50_r40000_lr0.01_hu128_bs16` ⭐ (Currently used - Best)
- `e50_r40000_lr0.01_hu256_bs16`

---

## 7. 📁 **DATA PROCESSING (ETL)**

### Extract, Transform, Load Operations

**Attraction ETL:**
- `attraction_etl.ipynb` - Processes attraction data
- Cleans and structures attraction information
- Processes reviews and ratings

**Hotel ETL:**
- `hotel_etl.ipynb` - Processes hotel data
- Removes duplicates
- Explodes amenities
- Creates user-hotel mappings

**Output:**
- Processed data in `etl/` folder
- JSON and Parquet formats
- Ready for model training

---

## 8. 🖼️ **IMAGE DOWNLOADING**

### Google Images Integration

**Features:**
- Automatically downloads images for attractions/hotels
- Uses Google Images API
- Stores in `downloads/` folder
- Fallback to default images if download fails

**Used in:**
- Attraction recommendations
- Hotel recommendations

---

## 9. 🎨 **INTERACTIVE UI**

### Jupyter Widgets Interface

**Features:**
- Interactive forms for user input
- Date pickers for trip dates
- Sliders for budget selection
- Button-based category/amenity selection
- Real-time recommendation display
- Image galleries
- Tabbed interface for multi-day trips

**Available in:**
- `get_att_recc.ipynb` - Attraction UI
- `final_hotel_recc.ipynb` - Hotel UI
- `sample_table_widget.ipynb` - Sample widget examples

---

## 📈 **Summary of All Features**

| Feature | Status | Technology | Input Required |
|---------|--------|------------|----------------|
| **Attraction Recommendations** | ✅ Working | RBM (Deep Learning) | Categories, Budget, Location, Dates |
| **Hotel Recommendations** | ✅ Available | Matrix Factorization (ALS) | Amenities, Destination, Dates |
| **Restaurant Recommendations** | ⚠️ Needs Dataset | Hybrid (K-Means + KNN) | Yelp Dataset |
| **Data Visualization** | ✅ Available | Matplotlib, Tableau | EDA Notebooks |
| **Web Scraping** | ✅ Available | BeautifulSoup, Selenium | TripAdvisor URLs |
| **Model Training** | ✅ Available | TensorFlow, PySpark | Training Notebooks |
| **Image Downloading** | ✅ Available | Google Images API | Automatic |
| **Interactive UI** | ✅ Available | Jupyter Widgets | Notebooks |

---

## 🚀 **Quick Start Guide**

### 1. Attractions (Working Now ✅)
```bash
python3 run_attractions_sample.py
# OR
# Open get_att_recc.ipynb in Jupyter
```

### 2. Hotels (Ready to Run)
```bash
# Open final_hotel_recc.ipynb in Jupyter
# Run all cells
# Select amenities
```

### 3. Restaurants (Need Dataset)
```bash
# 1. Download Yelp dataset
# 2. Place in yelp_dataset/ folder
# 3. Open Hybrid_Recommder.ipynb
```

### 4. Model Training
```bash
# Open rbm_training.ipynb
# Adjust parameters
# Train new models
```

---

## 💡 **Key Technologies Used**

- **Deep Learning:** TensorFlow, RBM
- **Big Data:** PySpark, ALS
- **Machine Learning:** Scikit-learn, K-Means, KNN
- **Data Processing:** Pandas, NumPy
- **Web Scraping:** BeautifulSoup, Selenium
- **Visualization:** Matplotlib, Seaborn, Tableau
- **UI:** Jupyter Widgets, IPython

---

## 📚 **Additional Resources**

- **Video Demo:** https://youtu.be/V635gdcw1h0
- **Project Report:** `report.pdf`
- **Poster:** `poster.pdf`
- **Running Guide:** `RUNNING_GUIDE.md`
- **Location Guide:** `LOCATION_GUIDE.md`

---

**This is a complete travel planning system that provides recommendations for attractions, hotels, and restaurants!** 🗺️✈️🏨🍽️

