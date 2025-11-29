# 🌐 Web Application Guide

## 🚀 Quick Start

### Option 1: Automatic Browser Opening
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
source setup_java11.sh
python3 start_server.py
```

The browser will open automatically at `http://localhost:5000`

### Option 2: Manual Start
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
source setup_java11.sh
python3 app.py
```

Then open your browser and go to: `http://localhost:5000`

### Option 3: Using Shell Script
```bash
./run_web_app.sh
```

---

## 🎯 Features

### Interactive Map
- **Leaflet.js** map with OpenStreetMap tiles
- **Color-coded markers**:
  - 🔴 Red = Hotels
  - 🔵 Blue = Attractions
  - 🟠 Orange = Restaurants

### Route Visualization
- **Optimized routes** shown as polylines on map
- **Day-by-day routes** with start/end markers
- **Click markers** to see details

### User Interface
- **Sidebar** with input form
- **Real-time recommendations** display
- **Weather forecast** badges
- **Statistics** (hotel/attraction/restaurant counts)
- **Responsive design** (works on mobile/tablet)

---

## 📋 How to Use

1. **Enter Your Information:**
   - Your name
   - Select destination city
   - Trip duration (days)
   - Total budget ($)

2. **Click "Get Recommendations"**

3. **View Results:**
   - Map shows all recommended locations
   - Routes are drawn between locations
   - Sidebar shows detailed recommendations
   - Weather forecast displayed

4. **Interact with Map:**
   - Click markers for details
   - Click recommendation cards to center map
   - Zoom and pan to explore

---

## 🗺️ Map Features

- **Markers**: Click to see name, rating, price, address
- **Routes**: Colored lines showing optimized paths
- **Zoom**: Use mouse wheel or +/- buttons
- **Pan**: Click and drag to move around

---

## 🎨 UI Components

### Input Form
- Name field
- City dropdown (10+ cities)
- Days selector (1-14 days)
- Budget input ($)

### Results Display
- **Stats**: Quick count of recommendations
- **Weather**: Forecast badges for trip dates
- **Hotels**: Cards with rating, price, address
- **Attractions**: Cards with details
- **Restaurants**: Cards organized by meal

---

## 🔧 Technical Details

### Backend
- **Flask** web framework
- **REST API** endpoints
- **Travel Planner** integration
- **Route optimization** algorithms

### Frontend
- **HTML5/CSS3** with Bootstrap 5
- **JavaScript** for interactivity
- **Leaflet.js** for maps
- **Font Awesome** icons

### APIs
- `/api/recommendations` - POST - Get travel plan
- `/api/cities` - GET - List available cities
- `/` - GET - Main page

---

## 🌍 Available Cities

- Vancouver (27 hotels)
- Quebec (752 hotels) ⭐ Best
- Saskatoon (54 hotels)
- Halifax (46 hotels)
- Montreal (3 hotels)
- Toronto (5 hotels)
- Victoria (29 hotels)
- Banff (21 hotels)
- Calgary (1 hotel)
- Ottawa (3 hotels)

---

## 🐛 Troubleshooting

### Map not showing?
- Check browser console for errors
- Ensure internet connection (for map tiles)
- Try refreshing the page

### No recommendations?
- Check city name spelling
- Try a different city
- Check server console for errors

### Server won't start?
- Ensure virtual environment is activated
- Check if port 5000 is available
- Run: `source setup_java11.sh` before starting

---

## 📱 Mobile Support

The UI is responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

---

## 🎉 Enjoy Your Travel Planning!

The web application provides a complete, interactive experience for planning your trip with visual maps and route optimization.

