#!/usr/bin/env python3
"""
Simple server startup script with automatic browser opening
"""
import webbrowser
import time
import threading
from app import app

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5001')

if __name__ == '__main__':
    print("=" * 70)
    print("🌍 AI Travel Recommendation System - Web Application")
    print("=" * 70)
    print("\n📍 Server starting at: http://localhost:5000")
    print("🌐 Browser will open automatically...")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)  # Disable debug to avoid import issues

