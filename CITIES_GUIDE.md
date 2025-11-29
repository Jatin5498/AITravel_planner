# 🏙️ Hotel Recommendations - Cities Guide

## 📍 Available Cities for Hotel Recommendations

This guide lists all cities available in the hotel dataset and how to use them.

---

## 🎯 How to Use Cities

### In Python Script:
```python
destination = "vancouver"  # Use lowercase city name
```

### In Jupyter Notebook:
Enter the city name in the "Destination" field (case-insensitive, but lowercase works best)

---

## 🇨🇦 Canadian Cities (Most Coverage)

### Major Cities with Most Hotels:

| City | Hotels | Usage |
|------|--------|-------|
| **quebec** | 752 | `destination = "quebec"` |
| **charlottetown** | 50 | `destination = "charlottetown"` |
| **saskatoon** | 54 | `destination = "saskatoon"` |
| **halifax** | 46 | `destination = "halifax"` |
| **st. john** | 47 | `destination = "st. john"` |

### Popular Tourist Destinations:

| City | Hotels | Usage |
|------|--------|-------|
| **vancouver** | 27 | `destination = "vancouver"` |
| **victoria** | 29 | `destination = "victoria"` |
| **banff** | 21 | `destination = "banff"` |
| **kelowna** | 27 | `destination = "kelowna"` |
| **regina** | 27 | `destination = "regina"` |
| **whitehorse** | 31 | `destination = "whitehorse"` |
| **yellowknife** | 19 | `destination = "yellowknife"` |

### Other Canadian Cities:

| City | Hotels | Usage |
|------|--------|-------|
| **montreal** | 3 | `destination = "montreal"` |
| **toronto** | 5 | `destination = "toronto"` |
| **ottawa** | 3 | `destination = "ottawa"` |
| **calgary** | 1 | `destination = "calgary"` |
| **edmonton** | 1 | `destination = "edmonton"` |
| **winnipeg** | 1 | `destination = "winnipeg"` |
| **whistler** | 1 | `destination = "whistler"` |
| **niagara** | 4 | `destination = "niagara"` |

---

## 🇺🇸 US Cities

| City | Hotels | Usage |
|------|--------|-------|
| **boston** | 1 | `destination = "boston"` |

---

## 📊 City Recommendations by Hotel Count

### Best Options (Most Hotels):
1. **quebec** - 752 hotels ⭐ BEST
2. **saskatoon** - 54 hotels
3. **charlottetown** - 50 hotels
4. **st. john** - 47 hotels
5. **halifax** - 46 hotels

### Good Options (20-30 hotels):
- **whitehorse** - 31 hotels
- **victoria** - 29 hotels
- **kelowna** - 27 hotels
- **regina** - 27 hotels
- **vancouver** - 27 hotels
- **banff** - 21 hotels
- **yellowknife** - 19 hotels

### Limited Options (1-5 hotels):
- **montreal** - 3 hotels
- **ottawa** - 3 hotels
- **toronto** - 5 hotels
- **niagara** - 4 hotels
- **calgary, edmonton, winnipeg, whistler, boston** - 1 hotel each

---

## 💡 Usage Examples

### Example 1: Quebec City (Best Coverage)
```python
destination = "quebec"  # 752 hotels available
```

### Example 2: Vancouver (Popular)
```python
destination = "vancouver"  # 27 hotels available
```

### Example 3: Banff (Tourist Destination)
```python
destination = "banff"  # 21 hotels available
```

### Example 4: Multiple Cities
```python
# Try different cities if one doesn't have enough results
destinations = ["quebec", "vancouver", "halifax", "saskatoon"]
for dest in destinations:
    # Run recommendations for each
    pass
```

---

## 🔍 How City Matching Works

The system searches for the city name in hotel addresses. It uses **case-insensitive substring matching**, so:

- ✅ `"vancouver"` matches: "vancouver", "North Vancouver", "Vancouver BC"
- ✅ `"montreal"` matches: "Montreal", "montreal quebec"
- ✅ `"st. john"` matches: "St. John's", "st. john newfoundland"

### Tips:
1. **Use lowercase** - Works best: `"vancouver"`
2. **Use city name only** - Don't include province/state
3. **Check spelling** - Use exact city name from the list above
4. **Try variations** - If "toronto" doesn't work, try "toronto ontario" (but usually just city name works)

---

## 🚨 Troubleshooting

### Issue: "No hotels found for destination 'X'"

**Solutions:**
1. **Check spelling** - Use exact city name from list above
2. **Try lowercase** - `"vancouver"` not `"Vancouver"`
3. **Use city name only** - Not "Vancouver, BC" or "Vancouver British Columbia"
4. **Try a different city** - Some cities have very few hotels
5. **Check available cities** - Use the list above

### Issue: "Only 1-2 hotels found"

**Solutions:**
1. **Use cities with more hotels** - Try "quebec" (752 hotels) or "saskatoon" (54 hotels)
2. **Remove destination filter** - Modify code to show all hotels (not filtered by city)
3. **Check amenities** - More specific amenities might reduce matches

---

## 📝 Quick Reference

### Copy-Paste Ready City Names:

```python
# Best coverage
"quebec"
"saskatoon"
"charlottetown"
"halifax"
"st. john"

# Popular destinations
"vancouver"
"victoria"
"banff"
"kelowna"
"whitehorse"

# Major cities (limited hotels)
"montreal"
"toronto"
"ottawa"
```

---

## 🎯 Recommended Cities for Testing

### For Best Results:
1. **quebec** - Most hotels (752)
2. **saskatoon** - Good coverage (54)
3. **vancouver** - Popular destination (27)
4. **halifax** - Good coverage (46)

### For Quick Testing:
- **vancouver** - Fast results, good variety
- **banff** - Tourist destination, good variety
- **victoria** - Good coverage, popular

---

## 🔧 Modifying the Script

To change the destination in `run_hotels_sample.py`:

```python
destination = "vancouver"  # Change this line
```

Or make it accept command-line arguments:

```python
import sys
destination = sys.argv[1] if len(sys.argv) > 1 else "vancouver"
```

Then run:
```bash
python3 run_hotels_sample.py quebec
python3 run_hotels_sample.py saskatoon
```

---

## 📊 Complete City List (Alphabetical)

1. banff (21 hotels)
2. boston (1 hotel)
3. calgary (1 hotel)
4. charlottetown (50 hotels)
5. edmonton (1 hotel)
6. halifax (46 hotels)
7. kelowna (27 hotels)
8. montreal (3 hotels)
9. niagara (4 hotels)
10. ottawa (3 hotels)
11. quebec (752 hotels) ⭐
12. regina (27 hotels)
13. saskatoon (54 hotels)
14. st. john (47 hotels)
15. toronto (5 hotels)
16. vancouver (27 hotels)
17. victoria (29 hotels)
18. whistler (1 hotel)
19. whitehorse (31 hotels)
20. winnipeg (1 hotel)
21. yellowknife (19 hotels)

---

## 💡 Pro Tips

1. **Start with "quebec"** - Highest chance of getting recommendations
2. **Use lowercase** - Always works better
3. **Check hotel count** - More hotels = better recommendations
4. **Try multiple cities** - If one doesn't work, try another
5. **Remove city filter** - For maximum results, modify code to show all hotels

---

**Total Cities Available: 21**  
**Total Hotels in Dataset: ~1,200+**

---

## 🚀 Quick Start

```bash
# Run with Quebec (best coverage)
python3 run_hotels_sample.py
# Then edit destination = "quebec" in the script

# Or use Jupyter notebook
jupyter notebook
# Open final_hotel_recc.ipynb
# Enter "quebec" in the Destination field
```

---

**Happy Hotel Hunting! 🏨**

