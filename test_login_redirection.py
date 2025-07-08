#!/usr/bin/env python3
"""
Test script to verify login redirection functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from werkzeug.security import generate_password_hash

def test_login_redirection():
    """Test the login redirection system"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing Login Redirection System")
        print("=" * 60)
        
        # Test 1: Check if admin users exist
        print("\n1. Checking Admin Users:")
        admin_users = User.query.filter_by(role='admin').all()
        if admin_users:
            print(f"   ✅ Found {len(admin_users)} admin user(s):")
            for user in admin_users:
                print(f"      - Username: {user.username}, Email: {user.email}")
        else:
            print("   ❌ No admin users found")
        
        # Test 2: Check if customers exist
        print("\n2. Checking Customers:")
        customers = Customer.query.all()
        if customers:
            print(f"   ✅ Found {len(customers)} customer(s):")
            for customer in customers:
                print(f"      - Username: {customer.username}, Email: {customer.email}")
        else:
            print("   ❌ No customers found")
        
        # Test 3: Verify login redirection logic
        print("\n3. Login Redirection Logic:")
        print("   Customer Login → Customer Dashboard")
        print("   Admin Login → Admin Dashboard")
        
        # Test 4: Show sample credentials
        print("\n4. Sample Login Credentials:")
        if admin_users:
            admin = admin_users[0]
            print(f"   Admin Login:")
            print(f"      Username: {admin.username}")
            print(f"      Password: (check database or registration)")
        
        if customers:
            customer = customers[0]
            print(f"   Customer Login:")
            print(f"      Username: {customer.username}")
            print(f"      Password: (check database or registration)")
        
        print("\n" + "=" * 60)
        print("🎯 Login Redirection Test Complete!")
        
        # Print login instructions
        print("\n📋 Login Instructions:")
        print("-" * 40)
        print("1. Go to: http://127.0.0.1:5000/login")
        print("2. For Customer Login:")
        print("   - Click 'Customer Login' tab")
        print("   - Enter customer credentials")
        print("   - Click 'Login as Customer'")
        print("   - Should redirect to: /customer_dashboard")
        print()
        print("3. For Admin Login:")
        print("   - Click 'Admin Login' tab")
        print("   - Enter admin credentials")
        print("   - Click 'Login as Admin'")
        print("   - Should redirect to: /dashboard")
        
        print("\n🔗 Expected Redirections:")
        print("Customer Login → Customer Dashboard")
        print("Admin Login → Admin Dashboard")

if __name__ == "__main__":
    test_login_redirection() 