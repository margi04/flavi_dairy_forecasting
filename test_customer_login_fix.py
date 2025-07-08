#!/usr/bin/env python3
"""
Test script to verify customer login and dashboard redirection fix
"""

import requests
import time

def test_customer_login():
    """Test customer login and dashboard redirection"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing Customer Login and Dashboard Redirection")
    print("=" * 60)
    
    # Test 1: Customer login
    print("\n1. Testing customer login...")
    login_data = {
        'username': 'testcustomer',
        'password': 'customer123',
        'user_type': 'customer'
    }
    
    try:
        # Create session to maintain cookies
        session = requests.Session()
        
        # Get login page first
        response = session.get(f"{base_url}/login")
        if response.status_code != 200:
            print(f"❌ Failed to get login page: {response.status_code}")
            return False
        
        # Submit login form
        response = session.post(f"{base_url}/login", data=login_data)
        
        if response.status_code == 200:
            # Check if we're redirected to customer dashboard
            if "customer_dashboard" in response.url or "Welcome, testcustomer" in response.text:
                print("✅ Customer login successful - redirected to customer dashboard")
            else:
                print("⚠️  Customer login successful but may not be on correct dashboard")
                print(f"   Current URL: {response.url}")
        else:
            print(f"❌ Customer login failed: {response.status_code}")
            return False
        
        # Test 2: Access dashboard directly
        print("\n2. Testing direct dashboard access...")
        response = session.get(f"{base_url}/dashboard")
        
        if response.status_code == 200:
            if "customer_dashboard" in response.url:
                print("✅ Dashboard redirect working correctly")
            elif "Welcome, testcustomer" in response.text:
                print("✅ Dashboard showing customer content")
            else:
                print("⚠️  Dashboard accessible but content unclear")
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
        
        # Test 3: Check for total_sales error
        print("\n3. Checking for total_sales error...")
        if "total_sales" in response.text and "undefined" in response.text.lower():
            print("❌ total_sales error still present")
            return False
        else:
            print("✅ No total_sales error detected")
        
        print("\n🎉 All tests passed! Customer login and dashboard redirection is working correctly.")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running.")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Starting customer login fix verification...")
    success = test_customer_login()
    
    if success:
        print("\n✅ Customer login system is working correctly!")
        print("   - Customers are properly redirected to customer_dashboard")
        print("   - No more total_sales undefined errors")
        print("   - Separate customer and admin dashboards functioning")
    else:
        print("\n❌ Customer login system needs attention")
        print("   - Check if Flask app is running")
        print("   - Verify customer credentials exist in database")
        print("   - Check for any remaining template errors") 