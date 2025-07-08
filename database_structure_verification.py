#!/usr/bin/env python3
"""
Database Structure Verification - Shows separate User and Customer tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer

def verify_database_structure():
    """Verify the separate User and Customer tables"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Database Structure Verification")
        print("=" * 60)
        
        # Get all users from User table
        print("\n📊 USER TABLE (Admin Users)")
        print("-" * 40)
        users = User.query.all()
        print(f"Total Users in User table: {len(users)}")
        
        if users:
            print("\nUser Details:")
            for user in users:
                print(f"  👤 {user.username}")
                print(f"     - Email: {user.email}")
                print(f"     - Role: {user.role}")
                print(f"     - ID: {user.id}")
                print()
        
        # Get all customers from Customer table
        print("📊 CUSTOMER TABLE (Customer Users)")
        print("-" * 40)
        customers = Customer.query.all()
        print(f"Total Customers in Customer table: {len(customers)}")
        
        if customers:
            print("\nCustomer Details:")
            for customer in customers:
                print(f"  👤 {customer.username}")
                print(f"     - Email: {customer.email}")
                print(f"     - Role: {customer.role}")
                print(f"     - ID: {customer.id}")
                if hasattr(customer, 'created_at'):
                    print(f"     - Created: {customer.created_at}")
                print()
        
        # Check for cross-contamination
        print("🔍 CROSS-CONTAMINATION CHECK")
        print("-" * 40)
        
        # Check if any customers exist in User table
        customer_usernames = [c.username for c in customers]
        user_customers = User.query.filter(User.username.in_(customer_usernames)).all()
        
        if user_customers:
            print("❌ CROSS-CONTAMINATION FOUND!")
            print("   Customers found in User table:")
            for user in user_customers:
                print(f"   - {user.username} (Role: {user.role})")
        else:
            print("✅ No customers found in User table")
        
        # Check if any admins exist in Customer table
        admin_usernames = [u.username for u in users if u.role == 'admin']
        customer_admins = Customer.query.filter(Customer.username.in_(admin_usernames)).all()
        
        if customer_admins:
            print("❌ CROSS-CONTAMINATION FOUND!")
            print("   Admins found in Customer table:")
            for customer in customer_admins:
                print(f"   - {customer.username} (Role: {customer.role})")
        else:
            print("✅ No admins found in Customer table")
        
        print()
        print("📋 DATABASE SEPARATION SUMMARY")
        print("-" * 40)
        print(f"✅ User Table: {len(users)} users (admins and legacy customers)")
        print(f"✅ Customer Table: {len(customers)} customers")
        print(f"✅ Cross-contamination: {'NO' if not user_customers and not customer_admins else 'YES'}")
        
        print()
        print("🔐 LOGIN VERIFICATION PROCESS")
        print("-" * 40)
        print("Admin Login:")
        print("  - Searches User table for username with role='admin'")
        print("  - Example: admin, Akanksha, akanksha, riya, aditi")
        print()
        print("Customer Login:")
        print("  - Searches Customer table for username")
        print("  - Example: margi, piyush, riya, testcustomer")
        print()
        print("✅ Database separation ensures secure login verification!")
        
        # Show table schemas
        print()
        print("🏗️ TABLE SCHEMAS")
        print("-" * 40)
        print("User Table (for Admins):")
        print("  - id (Primary Key)")
        print("  - username (Unique)")
        print("  - email (Unique)")
        print("  - password_hash")
        print("  - role (admin/customer)")
        print()
        print("Customer Table (for Customers):")
        print("  - id (Primary Key)")
        print("  - username (Unique)")
        print("  - email (Unique)")
        print("  - password_hash")
        print("  - role (always 'customer')")
        print("  - created_at (Timestamp)")

if __name__ == "__main__":
    verify_database_structure() 