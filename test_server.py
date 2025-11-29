#!/usr/bin/env python3
"""Test server to debug issues"""
from app import app
import sys

if __name__ == '__main__':
    print("=" * 70)
    print("Testing Flask App")
    print("=" * 70)
    
    # Test template rendering
    try:
        with app.test_client() as client:
            response = client.get('/')
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.data)}")
            if response.status_code == 200:
                print("✅ Template rendered successfully")
                # Save to file to check
                with open('test_output.html', 'w') as f:
                    f.write(response.data.decode('utf-8'))
                print("✅ Saved output to test_output.html")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.data.decode('utf-8')[:500])
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

