# Intelligent Travel Recommendation System - Running Guide

## 📋 What is This Project?

This is an **Intelligent Travel Recommendation System** that provides personalized travel recommendations using advanced machine learning techniques. The system recommends:

1. **Attractions** - Based on timing (morning/evening) and user preferences
2. **Hotels** - Based on amenities and user preferences  
3. **Restaurants** - Based on meal times (breakfast, lunch, dinner)

### 🎯 Key Features:
- **Personalized recommendations** based on user preferences
- **Multiple recommendation algorithms**:
  - **RBM (Restricted Boltzmann Machine)** - Deep learning for attractions
  - **Matrix Factorization with ALS** - Collaborative filtering for hotels
  - **Hybrid approach** - K-Means + KNN for restaurants
- **Interactive UI** using Jupyter widgets
- **Visual recommendations** with images and details

---

## 🚀 How to Run the Project

### Step 1: Access Jupyter Notebook

The Jupyter server is already running! Open your browser and go to:

```
http://localhost:8888/?token=377935ab77fd51d2b415c3e4d5ec70fa802d8f41b29c716b
```

**Note:** If the server stopped, restart it with:
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
jupyter notebook --no-browser --port=8888
```

### Step 2: Run Attraction Recommendations

1. **Open** `get_att_recc.ipynb` in Jupyter
2. **Run all cells** sequentially (Cell → Run All)
3. **Fill in the interactive form**:
   - User Name
   - Destination (Province)
   - Budget range (slider)
   - Start Date and End Date
   - **Select and rate at least 5 attraction categories** (click buttons and rate 0-5)
4. The system will:
   - Find a similar user based on your preferences
   - Load the trained RBM model
   - Generate personalized attraction recommendations
   - Display recommendations with images, locations, prices, and ratings

### Step 3: Run Hotel Recommendations

1. **Open** `final_hotel_recc.ipynb` in Jupyter
2. **Run all cells** sequentially
3. **Fill in the interactive form**:
   - User Name
   - Destination
   - Start Date and End Date
   - **Select at least 5 hotel amenities** (click buttons)
4. The system will:
   - Use Matrix Factorization (ALS) model
   - Match hotels based on your amenity preferences
   - Display top 5 hotel recommendations with details

### Step 4: Run Restaurant Recommendations (Optional)

1. **Open** `Hybrid_Recommder.ipynb` (if available)
2. **Note:** Requires Yelp dataset (see Data Requirements below)

---

## 📁 Project Structure

```
Intelligent-Travel-Recommendation-System/
├── get_att_recc.ipynb          # Main notebook for attraction recommendations
├── final_hotel_recc.ipynb      # Main notebook for hotel recommendations
├── rbm_training.ipynb          # Train/tune RBM model
├── hotel_etl.ipynb             # ETL for hotel data
├── attraction_etl.ipynb        # ETL for attraction data
├── attractions_recc.py         # Core attraction recommendation functions
├── hotel_recc.py               # Core hotel recommendation functions
├── rbm.py                       # RBM model implementation
├── utils.py                    # Utility functions
│
├── etl/                        # Processed data files
│   ├── attractions.json
│   ├── attraction_reviews.json
│   ├── del_dup/               # Hotel data (deduplicated)
│   ├── newh_df/               # Hotel data with amenities
│   └── u_id_df/               # User-hotel mappings
│
├── mf_models/                  # Pre-trained Matrix Factorization model
│   └── model_file/
│
├── recommendations/            # Pre-trained RBM models
│   └── e*_r*_lr*_hu*_bs*/     # Various model configurations
│
├── outputs/                    # Raw attraction data
└── downloads/                  # Downloaded attraction images
```

---

## 🔧 Further Steps & Customization

### 1. Train Your Own RBM Model

If you want to train a new RBM model with different parameters:

1. **Open** `rbm_training.ipynb`
2. **Modify parameters**:
   - `epochs`: Number of training epochs (default: 50)
   - `rows`: Number of data rows (default: 40000)
   - `alpha`: Learning rate (default: 0.01)
   - `H`: Number of hidden units (default: 128)
   - `batch_size`: Batch size (default: 16)
3. **Run the notebook** to train and save the model
4. **Update** `get_att_recc.ipynb` to use your new model

### 2. Retrain Hotel Model

1. **Open** `hotel_etl.ipynb` to process hotel data
2. **Open** `final_hotel_recc.ipynb`
3. The model will be retrained automatically when you run recommendations

### 3. Add Restaurant Recommendations

1. **Download Yelp dataset** from: https://www.yelp.ca/dataset/download
2. **Extract** to `yelp_dataset/` folder
3. **Open** `Hybrid_Recommder.ipynb` (if available)
4. **Run** to get restaurant recommendations

### 4. Customize Recommendations

**For Attractions:**
- Edit `attractions_recc.py`:
  - Modify `filter_df()` to change filtering logic
  - Adjust `find_closest()` for distance calculations
  - Change recommendation count in `final_output()`

**For Hotels:**
- Edit `hotel_recc.py`:
  - Modify `amenities_rating()` for amenity scoring
  - Adjust `model_train()` for ALS parameters
  - Change recommendation count in `get_hotel_output()`

### 5. View EDA Visualizations

Check the `EDA/` folder for exploratory data analysis visualizations:
- `a1.png` to `a9.png` - Attraction visualizations
- `h1.png` to `h5.png` - Hotel visualizations
- `r1.png` to `r8.png` - Restaurant visualizations

---

## 🐛 Troubleshooting

### Issue: Jupyter server not running
**Solution:**
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
jupyter notebook --no-browser --port=8888
```

### Issue: TensorFlow errors
**Solution:** The code has been updated to use TensorFlow 2.x compatibility mode. If you see errors, ensure you're using Python 3.12.

### Issue: Missing data files
**Solution:** 
- Attraction and hotel data should be in `etl/` folder (already present)
- For restaurants, download Yelp dataset

### Issue: PySpark errors
**Solution:** Ensure Java is installed:
```bash
brew install openjdk
```

### Issue: Model not found
**Solution:** 
- Pre-trained models are in `recommendations/` folder
- If missing, run `rbm_training.ipynb` to train a new model

---

## 📊 Model Parameters

### RBM Models Available:
- `e10_r5000_lr0.01_hu64_bs8` - 10 epochs, 5000 rows, 64 hidden units
- `e20_r20000_lr0.01_hu128_bs16` - 20 epochs, 20000 rows, 128 hidden units
- `e50_r40000_lr0.01_hu128_bs16` - 50 epochs, 40000 rows, 128 hidden units (recommended)

### Current Default in Code:
- Epochs: 50
- Rows: 40000
- Learning Rate: 0.01
- Hidden Units: 128
- Batch Size: 16

---

## 🎓 Understanding the Algorithms

### 1. RBM (Restricted Boltzmann Machine)
- **Purpose:** Attraction recommendations
- **How it works:** Learns hidden patterns in user-attraction interactions
- **Input:** User ratings on attraction categories
- **Output:** Personalized attraction scores

### 2. Matrix Factorization with ALS
- **Purpose:** Hotel recommendations
- **How it works:** Decomposes user-hotel matrix into latent factors
- **Input:** User preferences for hotel amenities
- **Output:** Hotel recommendations based on collaborative filtering

### 3. Hybrid Recommender
- **Purpose:** Restaurant recommendations
- **How it works:** Combines content-based (K-Means) and collaborative (KNN) filtering
- **Input:** Restaurant features and user preferences
- **Output:** Meal-specific restaurant recommendations

---

## 📝 Next Steps

1. ✅ **Run attraction recommendations** - Test the system
2. ✅ **Run hotel recommendations** - Test hotel matching
3. 🔄 **Train custom models** - Adjust parameters for better results
4. 🔄 **Add restaurant data** - Complete the full system
5. 🔄 **Customize UI** - Modify widgets and display format
6. 🔄 **Deploy** - Convert to web app (Flask/Streamlit)

---

## 📚 Additional Resources

- **Video Demo:** https://youtu.be/V635gdcw1h0
- **Project Report:** `report.pdf`
- **Poster:** `poster.pdf`
- **Yelp Dataset:** https://www.yelp.ca/dataset/download

---

## 💡 Tips

1. **Start with attraction recommendations** - It's the most complete feature
2. **Rate at least 5 categories** - More ratings = better recommendations
3. **Select diverse amenities** - For better hotel matching
4. **Check model performance** - View error plots in `recommendations/*/error.png`
5. **Experiment with parameters** - Train models with different settings

---

**Happy Travel Planning! 🗺️✈️**

