#!/usr/bin/env python3
"""
Complete Redirection System Test
Tests all redirection scenarios for the Flavi Dairy Forecasting AI application.
"""

import requests
import time
import json
from urllib.parse import urljoin

class RedirectionSystemTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {details}")
        
    def test_home_page(self):
        """Test home page accessibility"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200:
                self.log_test("Home Page Access", "PASS", "Home page loads successfully")
                return True
            else:
                self.log_test("Home Page Access", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Home Page Access", "ERROR", str(e))
            return False
    
    def test_login_page(self):
        """Test login page accessibility"""
        try:
            response = self.session.get(urljoin(self.base_url, "/login"))
            if response.status_code == 200:
                if "Customer Login" in response.text and "Admin Login" in response.text:
                    self.log_test("Login Page", "PASS", "Login page with tabs loads correctly")
                    return True
                else:
                    self.log_test("Login Page", "FAIL", "Login tabs not found")
                    return False
            else:
                self.log_test("Login Page", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Login Page", "ERROR", str(e))
            return False
    
    def test_customer_login_redirection(self):
        """Test customer login and redirection"""
        try:
            # Test customer login
            login_data = {
                'username': 'testcustomer',
                'password': 'password123',
                'login_type': 'customer'
            }
            
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data)
            
            if response.status_code == 200:
                # Check if redirected to customer dashboard
                if "customer_dashboard" in response.url or "/customer_dashboard" in response.text:
                    self.log_test("Customer Login Redirection", "PASS", "Customer redirected to customer dashboard")
                    return True
                else:
                    self.log_test("Customer Login Redirection", "FAIL", "Customer not redirected to correct dashboard")
                    return False
            else:
                self.log_test("Customer Login Redirection", "FAIL", f"Login failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Customer Login Redirection", "ERROR", str(e))
            return False
    
    def test_admin_login_redirection(self):
        """Test admin login and redirection"""
        try:
            # Test admin login
            login_data = {
                'username': 'admin',
                'password': 'admin123',
                'login_type': 'admin'
            }
            
            response = self.session.post(urljoin(self.base_url, "/login"), data=login_data)
            
            if response.status_code == 200:
                # Check if redirected to admin dashboard
                if "dashboard" in response.url or "/dashboard" in response.text:
                    self.log_test("Admin Login Redirection", "PASS", "Admin redirected to admin dashboard")
                    return True
                else:
                    self.log_test("Admin Login Redirection", "FAIL", "Admin not redirected to correct dashboard")
                    return False
            else:
                self.log_test("Admin Login Redirection", "FAIL", f"Login failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Admin Login Redirection", "ERROR", str(e))
            return False
    
    def test_dashboard_access_control(self):
        """Test dashboard access control"""
        try:
            # Test accessing admin dashboard as customer
            response = self.session.get(urljoin(self.base_url, "/dashboard"))
            
            if response.status_code == 200:
                if "customer_dashboard" in response.url:
                    self.log_test("Dashboard Access Control", "PASS", "Customer redirected from admin dashboard")
                else:
                    self.log_test("Dashboard Access Control", "FAIL", "Customer not redirected from admin dashboard")
                    return False
            else:
                self.log_test("Dashboard Access Control", "FAIL", f"Dashboard access failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Access Control", "ERROR", str(e))
            return False
    
    def test_customer_dashboard_access(self):
        """Test customer dashboard access"""
        try:
            response = self.session.get(urljoin(self.base_url, "/customer_dashboard"))
            
            if response.status_code == 200:
                if "customer_dashboard" in response.text or "My Orders" in response.text:
                    self.log_test("Customer Dashboard Access", "PASS", "Customer dashboard loads correctly")
                    return True
                else:
                    self.log_test("Customer Dashboard Access", "FAIL", "Customer dashboard content not found")
                    return False
            else:
                self.log_test("Customer Dashboard Access", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Customer Dashboard Access", "ERROR", str(e))
            return False
    
    def test_profile_redirection(self):
        """Test profile page redirection"""
        try:
            response = self.session.get(urljoin(self.base_url, "/profile"))
            
            if response.status_code == 200:
                if "customer_profile" in response.url:
                    self.log_test("Profile Redirection", "PASS", "Profile redirects to customer profile")
                    return True
                else:
                    self.log_test("Profile Redirection", "FAIL", "Profile not redirecting correctly")
                    return False
            else:
                self.log_test("Profile Redirection", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Profile Redirection", "ERROR", str(e))
            return False
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        try:
            response = self.session.get(urljoin(self.base_url, "/logout"))
            
            if response.status_code == 200:
                # Check if redirected to home page
                if self.base_url in response.url or "index" in response.url:
                    self.log_test("Logout Functionality", "PASS", "Logout successful and redirected to home")
                    return True
                else:
                    self.log_test("Logout Functionality", "FAIL", "Logout not redirecting to home")
                    return False
            else:
                self.log_test("Logout Functionality", "FAIL", f"Logout failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Logout Functionality", "ERROR", str(e))
            return False
    
    def test_registration_redirection(self):
        """Test registration page redirection"""
        try:
            # Test customer registration page
            response = self.session.get(urljoin(self.base_url, "/customer_register"))
            
            if response.status_code == 200:
                if "Register as Customer" in response.text:
                    self.log_test("Customer Registration Page", "PASS", "Customer registration page loads")
                else:
                    self.log_test("Customer Registration Page", "FAIL", "Customer registration form not found")
                    return False
            
            # Test admin registration page
            response = self.session.get(urljoin(self.base_url, "/admin_register"))
            
            if response.status_code == 200:
                if "Register as Admin" in response.text:
                    self.log_test("Admin Registration Page", "PASS", "Admin registration page loads")
                    return True
                else:
                    self.log_test("Admin Registration Page", "FAIL", "Admin registration form not found")
                    return False
            else:
                self.log_test("Admin Registration Page", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Registration Redirection", "ERROR", str(e))
            return False
    
    def test_navigation_links(self):
        """Test navigation links in templates"""
        try:
            # Test customer navigation
            response = self.session.get(urljoin(self.base_url, "/customer_dashboard"))
            
            if response.status_code == 200:
                # Check for customer-specific navigation links
                if "My Orders" in response.text and "Order History" in response.text:
                    self.log_test("Customer Navigation", "PASS", "Customer navigation links present")
                else:
                    self.log_test("Customer Navigation", "FAIL", "Customer navigation links missing")
                    return False
            
            # Test admin navigation (if we can access it)
            response = self.session.get(urljoin(self.base_url, "/dashboard"))
            
            if response.status_code == 200:
                # Check for admin-specific navigation links
                if "SKUs" in response.text or "Orders" in response.text or "Users" in response.text:
                    self.log_test("Admin Navigation", "PASS", "Admin navigation links present")
                    return True
                else:
                    self.log_test("Admin Navigation", "FAIL", "Admin navigation links missing")
                    return False
            else:
                self.log_test("Admin Navigation", "SKIP", "Cannot access admin dashboard for navigation test")
                return True
                
        except Exception as e:
            self.log_test("Navigation Links", "ERROR", str(e))
            return False
    
    def run_all_tests(self):
        """Run all redirection tests"""
        print("🚀 Starting Complete Redirection System Test")
        print("=" * 60)
        
        tests = [
            self.test_home_page,
            self.test_login_page,
            self.test_customer_login_redirection,
            self.test_admin_login_redirection,
            self.test_dashboard_access_control,
            self.test_customer_dashboard_access,
            self.test_profile_redirection,
            self.test_logout_functionality,
            self.test_registration_redirection,
            self.test_navigation_links
        ]
        
        passed = 0
        failed = 0
        errors = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test.__name__, "ERROR", str(e))
                errors += 1
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"📈 Total: {passed + failed + errors}")
        
        # Save results to file
        with open("redirection_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: redirection_test_results.json")
        
        return passed, failed, errors

def main():
    """Main function to run the tests"""
    print("🔍 Flavi Dairy Forecasting AI - Complete Redirection System Test")
    print("This test verifies all redirection scenarios for customers and admins.")
    print()
    
    # Check if app is running
    tester = RedirectionSystemTester()
    
    try:
        # Test if app is accessible
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code != 200:
            print("❌ Application is not running on http://127.0.0.1:5000")
            print("Please start the application first:")
            print("   python run.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application on http://127.0.0.1:5000")
        print("Please start the application first:")
        print("   python run.py")
        return
    
    print("✅ Application is running. Starting tests...")
    print()
    
    # Run all tests
    passed, failed, errors = tester.run_all_tests()
    
    print()
    if failed == 0 and errors == 0:
        print("🎉 All tests passed! The redirection system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the detailed results above.")
    
    print("\n📋 Test Coverage:")
    print("- Home page accessibility")
    print("- Login page with tabs")
    print("- Customer login and redirection")
    print("- Admin login and redirection")
    print("- Dashboard access control")
    print("- Customer dashboard access")
    print("- Profile page redirection")
    print("- Logout functionality")
    print("- Registration page redirection")
    print("- Navigation links verification")

if __name__ == "__main__":
    main() 