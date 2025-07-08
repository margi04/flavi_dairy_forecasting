#!/usr/bin/env python3
"""
Test script to verify customer and admin login verification system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from werkzeug.security import generate_password_hash

def test_login_verification():
    """Test the login verification system for both customers and admins"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing Customer and Admin Login Verification System")
        print("=" * 60)
        
        # Test 1: Check if admin users exist in User table
        print("\n1. Checking Admin Users in User table:")
        admin_users = User.query.filter_by(role='admin').all()
        if admin_users:
            print(f"   ✅ Found {len(admin_users)} admin user(s):")
            for user in admin_users:
                print(f"      - Username: {user.username}, Email: {user.email}, Role: {user.role}")
        else:
            print("   ❌ No admin users found in User table")
        
        # Test 2: Check if customers exist in Customer table
        print("\n2. Checking Customers in Customer table:")
        customers = Customer.query.all()
        if customers:
            print(f"   ✅ Found {len(customers)} customer(s):")
            for customer in customers:
                print(f"      - Username: {customer.username}, Email: {customer.email}, Role: {customer.role}")
        else:
            print("   ❌ No customers found in Customer table")
        
        # Test 3: Test admin login verification
        print("\n3. Testing Admin Login Verification:")
        if admin_users:
            test_admin = admin_users[0]
            print(f"   Testing with admin: {test_admin.username}")
            
            # Test correct password
            if test_admin.check_password('admin123'):  # Assuming this is the default password
                print("   ✅ Admin password verification works correctly")
            else:
                print("   ❌ Admin password verification failed")
            
            # Test wrong password
            if not test_admin.check_password('wrongpassword'):
                print("   ✅ Admin wrong password rejection works correctly")
            else:
                print("   ❌ Admin wrong password acceptance (security issue)")
        else:
            print("   ⚠️  Skipping admin test - no admin users found")
        
        # Test 4: Test customer login verification
        print("\n4. Testing Customer Login Verification:")
        if customers:
            test_customer = customers[0]
            print(f"   Testing with customer: {test_customer.username}")
            
            # Test correct password
            if test_customer.check_password('customer123'):  # Assuming this is the default password
                print("   ✅ Customer password verification works correctly")
            else:
                print("   ❌ Customer password verification failed")
            
            # Test wrong password
            if not test_customer.check_password('wrongpassword'):
                print("   ✅ Customer wrong password rejection works correctly")
            else:
                print("   ❌ Customer wrong password acceptance (security issue)")
        else:
            print("   ⚠️  Skipping customer test - no customers found")
        
        # Test 5: Test database separation
        print("\n5. Testing Database Table Separation:")
        
        # Check that customers are not in User table
        customer_usernames = [c.username for c in customers]
        user_customers = User.query.filter(User.username.in_(customer_usernames)).all()  # type: ignore
        if not user_customers:
            print("   ✅ Customer data is properly separated (not in User table)")
        else:
            print("   ❌ Customer data found in User table (separation issue)")
        
        # Check that admins are not in Customer table
        admin_usernames = [a.username for a in admin_users]
        customer_admins = Customer.query.filter(Customer.username.in_(admin_usernames)).all()  # type: ignore
        if not customer_admins:
            print("   ✅ Admin data is properly separated (not in Customer table)")
        else:
            print("   ❌ Admin data found in Customer table (separation issue)")
        
        print("\n" + "=" * 60)
        print("🎯 Login Verification System Test Complete!")
        
        # Print sample credentials for testing
        print("\n📋 Sample Login Credentials for Testing:")
        print("-" * 40)
        if admin_users:
            print("Admin Users:")
            for user in admin_users[:3]:  # Show first 3 admins
                print(f"  Username: {user.username}")
        if customers:
            print("Customer Users:")
            for customer in customers[:3]:  # Show first 3 customers
                print(f"  Username: {customer.username}")

if __name__ == "__main__":
    test_login_verification() 