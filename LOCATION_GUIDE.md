# Location & Budget Guide

## ⚠️ Issue with India

**Problem:** India has only **1 attraction** priced at **$40.90**, but your minimum budget is **$50.00**, so it gets filtered out.

**Solutions:**
1. **Lower your budget_min** to $40 or less
2. **Choose a different location** with more attractions (see recommendations below)

---

## 📍 Best Locations (Most Attractions)

### Top 10 Locations by Number of Attractions:

1. **british_columbia** - 1,346 attractions | Price: $7.09 - $999.00
2. **ontario** - 688 attractions | Price: $6.80 - $999.00  
3. **quebec** - 497 attractions | Price: $5.00 - $886.09
4. **alberta** - 312 attractions | Price: $7.50 - $949.00
5. **nova_scotia** - 136 attractions | Price: $12.00 - $914.25
6. **new_york_(ny)** - 61 attractions | Price: $29.99 - $952.92
7. **prince_edward_island** - 39 attractions | Price: $15.75 - $670.00
8. **italy** - 39 attractions | Price: $46.37 - $886.09
9. **yukon** - 39 attractions | Price: $114.45 - $702.45
10. **northwest_territories** - 29 attractions | Price: $55.00 - $982.00

### International Locations with Good Coverage:

- **italy** - 39 attractions | $46.37 - $886.09
- **spain** - 20 attractions | $46.37 - $886.09
- **france** - 20 attractions | $46.37 - $886.09
- **japan** - 15 attractions | $47.71 - $886.09
- **united_kingdom_(uk)** - 16 attractions | $46.37 - $886.09
- **australia** - Available (check exact count)
- **thailand** - Available (check exact count)

---

## 🔧 Quick Fixes for Your Current Settings

### Option 1: Lower Budget for India
```python
province = "india"
budget_min = 40.0  # Lower than $40.90
budget_max = 50000.0
```

### Option 2: Use a Location with More Attractions
```python
# Best options:
province = "british_columbia"  # 1,346 attractions
# OR
province = "ontario"  # 688 attractions
# OR
province = "quebec"  # 497 attractions

budget_min = 50.0
budget_max = 50000.0
```

### Option 3: Use International Location
```python
province = "italy"  # 39 attractions
# OR
province = "spain"  # 20 attractions
# OR
province = "france"  # 20 attractions

budget_min = 50.0
budget_max = 50000.0
```

---

## 📊 All Available Locations

The dataset contains **97 unique locations** including:

### Canadian Provinces:
- british_columbia, ontario, quebec, alberta, nova_scotia, manitoba, new_brunswick, newfoundland_and_labrador, prince_edward_island, northwest_territories, yukon

### US States:
- california_(ca), new_york_(ny), washington_(wa), hawaii_(hi), florida_(fl), alaska_(ak), illinois_(il), massachusetts_(ma), maryland_(md), nevada_(nv), pennsylvania_(pa), louisiana_(la), south_carolina_(sc), district_of_columbia_(dc), new_hampshire_(nh)

### Countries:
- india, indonesia, italy, japan, spain, france, australia, thailand, china, south_korea, singapore, malaysia, turkey, greece, portugal, germany, austria, switzerland, netherlands, united_kingdom_(uk), ireland, iceland, norway, sweden, denmark, finland, russia, poland, czech_republic, croatia, serbia, egypt, morocco, south_africa, mauritius, brazil, argentina, chile, colombia, costa_rica, panama, dominican_republic, jamaica, bahamas, puerto_rico, israel, uae, and more...

---

## 💡 Recommendations

**For best results, use:**
- **british_columbia** or **ontario** - Most attractions, wide price range
- Budget: $50 - $500 (or higher if needed)
- These locations have hundreds of options across all categories

**For international travel:**
- **italy**, **spain**, or **france** - Good coverage, reasonable prices
- Budget: $50 - $1000

**For India specifically:**
- Lower budget_min to $40 or less
- Or wait for more India attractions to be added to the dataset

---

## 🛠️ How to Check Available Locations

Run this command to see all locations:
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
python3 -c "import pandas as pd; df = pd.read_json('etl/attractions.json', orient='records'); print(sorted(df['province'].unique()))"
```

