# ☕ Java 11 Setup for Hotel Recommendations

## ✅ Installation Complete!

Java 11 has been installed and configured for this project. The system will now use Java 11 instead of Java 25 for PySpark operations.

## 🚀 How to Use

### Option 1: Use the Setup Script (Recommended)
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
source setup_java11.sh
python3 run_hotels_sample.py
```

### Option 2: Use the Enhanced Activation Script
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate_java11
python3 run_hotels_sample.py
```

### Option 3: Automatic (Script Handles It)
The `run_hotels_sample.py` script now automatically detects and uses Java 11:
```bash
cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
python3 run_hotels_sample.py
```

## 📋 What Was Installed

- **Java 11 (OpenJDK 11.0.29)** - Compatible with PySpark
- **Location:** `/opt/homebrew/opt/openjdk@11/`

## 🔧 Files Created

1. **`setup_java11.sh`** - Script to configure Java 11 environment
2. **`venv/bin/activate_java11`** - Enhanced venv activation with Java 11
3. **Updated `run_hotels_sample.py`** - Auto-detects and uses Java 11

## ✅ Verification

To verify Java 11 is being used:
```bash
source setup_java11.sh
java -version
# Should show: openjdk version "11.0.29"
```

## 🎯 Next Steps

Now you can run hotel recommendations:
```bash
python3 run_hotels_sample.py
```

Or use the Jupyter notebook:
```bash
jupyter notebook
# Open: final_hotel_recc.ipynb
```

## 💡 Notes

- Java 11 is installed system-wide but only used when you source `setup_java11.sh`
- The script automatically sets `JAVA_HOME` and updates `PATH`
- Your system Java 25 remains unchanged - only this project uses Java 11
- If you want Java 11 globally, add to `~/.zshrc`:
  ```bash
  export JAVA_HOME="/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home"
  export PATH="$JAVA_HOME/bin:$PATH"
  ```

---

**Java 11 is ready! You can now run hotel recommendations without Java compatibility issues.** 🎉

