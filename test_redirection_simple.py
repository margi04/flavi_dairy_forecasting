#!/usr/bin/env python3
"""
Simple Redirection Test
Tests the basic redirection functionality using built-in libraries.
"""

import urllib.request
import urllib.parse
import urllib.error
import time

def test_basic_redirection():
    """Test basic redirection functionality"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Testing Basic Redirection System")
    print("=" * 50)
    
    try:
        # Test 1: Home page
        print("1. Testing home page...")
        try:
            response = urllib.request.urlopen(f"{base_url}/", timeout=5)
            if response.getcode() == 200:
                print("   ✅ Home page loads successfully")
            else:
                print(f"   ❌ Home page failed: {response.getcode()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Home page failed: {e.code}")
            return False
        
        # Test 2: Login page
        print("2. Testing login page...")
        try:
            response = urllib.request.urlopen(f"{base_url}/login", timeout=5)
            if response.getcode() == 200:
                content = response.read().decode('utf-8')
                if "Customer Login" in content and "Admin Login" in content:
                    print("   ✅ Login page with tabs loads correctly")
                else:
                    print("   ❌ Login tabs not found")
                    return False
            else:
                print(f"   ❌ Login page failed: {response.getcode()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Login page failed: {e.code}")
            return False
        
        # Test 3: Customer registration page
        print("3. Testing customer registration page...")
        try:
            response = urllib.request.urlopen(f"{base_url}/customer_register", timeout=5)
            if response.getcode() == 200:
                print("   ✅ Customer registration page loads")
            else:
                print(f"   ❌ Customer registration page failed: {response.getcode()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Customer registration page failed: {e.code}")
            return False
        
        # Test 4: Admin registration page
        print("4. Testing admin registration page...")
        try:
            response = urllib.request.urlopen(f"{base_url}/admin_register", timeout=5)
            if response.getcode() == 200:
                print("   ✅ Admin registration page loads")
            else:
                print(f"   ❌ Admin registration page failed: {response.getcode()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Admin registration page failed: {e.code}")
            return False
        
        # Test 5: Try to access customer dashboard without login
        print("5. Testing customer dashboard access without login...")
        try:
            response = urllib.request.urlopen(f"{base_url}/customer_dashboard", timeout=5)
            print(f"   ❌ Customer dashboard should redirect but returned: {response.getcode()}")
            return False
        except urllib.error.HTTPError as e:
            if e.code == 302:  # Should redirect to login
                print("   ✅ Customer dashboard properly redirects to login when not authenticated")
            else:
                print(f"   ❌ Customer dashboard access issue: {e.code}")
                return False
        
        # Test 6: Try to access admin dashboard without login
        print("6. Testing admin dashboard access without login...")
        try:
            response = urllib.request.urlopen(f"{base_url}/dashboard", timeout=5)
            print(f"   ❌ Admin dashboard should redirect but returned: {response.getcode()}")
            return False
        except urllib.error.HTTPError as e:
            if e.code == 302:  # Should redirect to login
                print("   ✅ Admin dashboard properly redirects to login when not authenticated")
            else:
                print(f"   ❌ Admin dashboard access issue: {e.code}")
                return False
        
        print("\n🎉 All basic redirection tests passed!")
        print("\n📋 Next Steps:")
        print("1. Test customer login with valid credentials")
        print("2. Test admin login with valid credentials")
        print("3. Verify proper redirection after login")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ Cannot connect to application: {e}")
        print("Make sure it's running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_login_redirection():
    """Test login redirection with test credentials"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n🔍 Testing Login Redirection")
    print("=" * 50)
    
    try:
        # Test customer login
        print("1. Testing customer login...")
        login_data = {
            'username': 'testcustomer',
            'password': 'password123',
            'login_type': 'customer'
        }
        
        data = urllib.parse.urlencode(login_data).encode('utf-8')
        req = urllib.request.Request(f"{base_url}/login", data=data, method='POST')
        
        try:
            response = urllib.request.urlopen(req, timeout=5)
            content = response.read().decode('utf-8')
            if "customer_dashboard" in response.geturl() or "/customer_dashboard" in content:
                print("   ✅ Customer login redirects to customer dashboard")
            else:
                print("   ❌ Customer login not redirecting correctly")
                print(f"   Response URL: {response.geturl()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Customer login failed: {e.code}")
            return False
        
        # Test admin login
        print("2. Testing admin login...")
        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'login_type': 'admin'
        }
        
        data = urllib.parse.urlencode(login_data).encode('utf-8')
        req = urllib.request.Request(f"{base_url}/login", data=data, method='POST')
        
        try:
            response = urllib.request.urlopen(req, timeout=5)
            content = response.read().decode('utf-8')
            if "dashboard" in response.geturl() or "/dashboard" in content:
                print("   ✅ Admin login redirects to admin dashboard")
            else:
                print("   ❌ Admin login not redirecting correctly")
                print(f"   Response URL: {response.geturl()}")
                return False
        except urllib.error.HTTPError as e:
            print(f"   ❌ Admin login failed: {e.code}")
            return False
        
        print("\n🎉 All login redirection tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Login test failed with error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Flavi Dairy Forecasting AI - Simple Redirection Test")
    print("=" * 60)
    
    # Test basic functionality
    if test_basic_redirection():
        print("\n✅ Basic redirection system is working!")
        
        # Ask if user wants to test login
        print("\nWould you like to test login redirection? (y/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice in ['y', 'yes']:
                test_login_redirection()
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user.")
    else:
        print("\n❌ Basic redirection system has issues!")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the application is running: python run.py")
        print("2. Check if the server is accessible at http://127.0.0.1:5000")
        print("3. Check the application logs for errors")
        print("4. Verify database connection")

if __name__ == "__main__":
    main() 