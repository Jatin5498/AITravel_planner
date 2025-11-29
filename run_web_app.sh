#!/bin/bash
# Script to run the web application

cd /Users/pranavmittal/Downloads/Intelligent-Travel-Recommendation-System
source venv/bin/activate
source setup_java11.sh

echo "=" | head -c 70
echo ""
echo "🌍 Starting AI Travel Recommendation Web Application"
echo "=" | head -c 70
echo ""
echo "📍 Server will start at: http://localhost:5000"
echo "🌐 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py

