#!/usr/bin/env python3
"""
Script to check and test customer passwords
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import Customer
from werkzeug.security import generate_password_hash, check_password_hash

def test_customer_passwords():
    """Test customer passwords and show available credentials"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing Customer Passwords")
        print("=" * 50)
        
        # Get all customers
        customers = Customer.query.all()
        
        if not customers:
            print("❌ No customers found in database")
            return
        
        print(f"✅ Found {len(customers)} customer(s)")
        print()
        
        # Test common passwords
        common_passwords = [
            'customer123',
            'password',
            '123456',
            'customer',
            'margi123',
            'piyush123',
            'riya123',
            'admin123',
            'test123'
        ]
        
        for customer in customers:
            print(f"👤 Customer: {customer.username} ({customer.email})")
            print(f"   Password Hash: {customer.password_hash[:20]}...")
            
            # Test each common password
            for password in common_passwords:
                if customer.check_password(password):
                    print(f"   ✅ Password found: '{password}'")
                    break
            else:
                print(f"   ❌ Password not found in common passwords")
            
            print()
        
        # Create a test customer with known password
        print("🔧 Creating test customer with known password...")
        test_customer = Customer.query.filter_by(username='testcustomer').first()
        
        if not test_customer:
            test_customer = Customer(
                username='testcustomer',
                email='test@example.com'
            )
            test_customer.set_password('customer123')
            db.session.add(test_customer)
            db.session.commit()
            print("✅ Test customer created with password: 'customer123'")
        else:
            print("✅ Test customer already exists")
        
        print()
        print("📋 Available Customer Credentials for Testing:")
        print("-" * 50)
        
        for customer in customers:
            print(f"Username: {customer.username}")
            print(f"Email: {customer.email}")
            print()
        
        print("🔑 Test Customer (if created):")
        print("Username: testcustomer")
        print("Password: customer123")
        print()
        print("💡 Try these credentials in the login form!")

if __name__ == "__main__":
    test_customer_passwords() 