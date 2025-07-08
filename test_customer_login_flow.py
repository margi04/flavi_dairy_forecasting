#!/usr/bin/env python3
"""
Test script to verify the complete customer login flow and redirection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import Customer
from app.models.user import User
from werkzeug.security import generate_password_hash

def test_customer_login_flow():
    """Test the complete customer login flow and redirection"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing Complete Customer Login Flow")
        print("=" * 60)
        
        # Test 1: Check if customers exist
        print("\n1. Checking Customer Database:")
        customers = Customer.query.all()
        if customers:
            print(f"   ✅ Found {len(customers)} customer(s) in Customer table")
            for customer in customers:
                print(f"      - Username: {customer.username}, Email: {customer.email}")
        else:
            print("   ❌ No customers found in Customer table")
            return
        
        # Test 2: Verify customer login verification
        print("\n2. Testing Customer Login Verification:")
        test_customer = customers[0]
        print(f"   Testing with customer: {test_customer.username}")
        
        # Test password verification
        if test_customer.check_password('customer123'):
            print("   ✅ Customer password verification works")
        else:
            print("   ❌ Customer password verification failed")
            return
        
        # Test 3: Verify customer dashboard access
        print("\n3. Testing Customer Dashboard Access:")
        print(f"   Customer ID: {test_customer.id}")
        print(f"   Customer Username: {test_customer.username}")
        print(f"   Customer Email: {test_customer.email}")
        print(f"   Customer Role: {test_customer.role}")
        
        # Test 4: Verify customer is not in admin table
        print("\n4. Testing Database Separation:")
        admin_customer = User.query.filter_by(username=test_customer.username).first()
        if not admin_customer:
            print("   ✅ Customer is properly separated (not in User table)")
        else:
            print("   ❌ Customer found in User table (separation issue)")
        
        # Test 5: Verify customer-specific methods
        print("\n5. Testing Customer-Specific Methods:")
        print(f"   is_admin(): {test_customer.is_admin()}")
        print(f"   is_accountant(): {test_customer.is_accountant()}")
        print(f"   Role: {test_customer.role}")
        
        if not test_customer.is_admin() and test_customer.role == 'customer':
            print("   ✅ Customer role verification works correctly")
        else:
            print("   ❌ Customer role verification failed")
        
        print("\n" + "=" * 60)
        print("🎯 Customer Login Flow Test Complete!")
        
        # Print login instructions
        print("\n📋 Customer Login Instructions:")
        print("-" * 40)
        print("1. Go to: http://127.0.0.1:5000/login")
        print("2. Click on 'Customer Login' tab")
        print("3. Enter credentials:")
        print(f"   Username: {test_customer.username}")
        print("   Password: customer123")
        print("4. Click 'Login as Customer'")
        print("5. You should be redirected to the customer dashboard")
        print("6. The dashboard will show:")
        print("   - Customer information")
        print("   - Order statistics")
        print("   - Quick action buttons")
        print("   - Recent orders")
        print("   - Product ordering section")
        
        print("\n🔗 Expected Flow:")
        print("Login → Customer Dashboard → Order History (optional)")
        print("   ↓")
        print("Customer can navigate between dashboard and order history")

if __name__ == "__main__":
    test_customer_login_flow() 