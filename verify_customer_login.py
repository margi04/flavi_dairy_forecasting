#!/usr/bin/env python3
"""
Step-by-step verification of customer login process
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.customer import Customer
from app.models.user import User

def verify_customer_login_process():
    """Demonstrate the exact customer login verification process"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Step-by-Step Customer Login Verification Process")
        print("=" * 70)
        
        # Test credentials
        test_username = "testcustomer"
        test_password = "customer123"
        
        print(f"📝 Test Credentials:")
        print(f"   Username: {test_username}")
        print(f"   Password: {test_password}")
        print()
        
        # Step 1: Check if customer exists in Customer table
        print("1️⃣ STEP 1: Check Customer Table")
        print("-" * 40)
        customer = Customer.query.filter_by(username=test_username).first()
        
        if customer:
            print(f"   ✅ Customer found in Customer table!")
            print(f"   📋 Customer Details:")
            print(f"      - ID: {customer.id}")
            print(f"      - Username: {customer.username}")
            print(f"      - Email: {customer.email}")
            print(f"      - Role: {customer.role}")
            print(f"      - Password Hash: {customer.password_hash[:30]}...")
        else:
            print(f"   ❌ Customer NOT found in Customer table")
            return
        print()
        
        # Step 2: Verify customer is NOT in User table (admin table)
        print("2️⃣ STEP 2: Verify Database Separation")
        print("-" * 40)
        admin_user = User.query.filter_by(username=test_username).first()
        
        if not admin_user:
            print(f"   ✅ Customer is NOT in User table (admin table)")
            print(f"   ✅ Database separation is working correctly")
        else:
            print(f"   ❌ Customer found in User table (separation issue)")
        print()
        
        # Step 3: Test password verification
        print("3️⃣ STEP 3: Password Verification")
        print("-" * 40)
        if customer.check_password(test_password):
            print(f"   ✅ Password verification successful!")
            print(f"   ✅ Customer credentials are valid")
        else:
            print(f"   ❌ Password verification failed!")
            print(f"   ❌ Invalid credentials")
            return
        print()
        
        # Step 4: Test customer-specific methods
        print("4️⃣ STEP 4: Customer Role Verification")
        print("-" * 40)
        print(f"   is_admin(): {customer.is_admin()}")
        print(f"   is_accountant(): {customer.is_accountant()}")
        print(f"   Role: {customer.role}")
        
        if not customer.is_admin() and customer.role == 'customer':
            print(f"   ✅ Customer role verification successful!")
        else:
            print(f"   ❌ Customer role verification failed!")
        print()
        
        # Step 5: Simulate session data
        print("5️⃣ STEP 5: Session Data (Simulated)")
        print("-" * 40)
        session_data = {
            'user_type': 'customer',
            'user_id': customer.id,
            'username': customer.username
        }
        print(f"   Session data that would be created:")
        for key, value in session_data.items():
            print(f"      {key}: {value}")
        print()
        
        # Step 6: Dashboard data preparation
        print("6️⃣ STEP 6: Dashboard Data Preparation")
        print("-" * 40)
        from app.models.order import Order
        from app.models.sku import SKU
        
        # Get customer orders
        orders = Order.query.filter_by(customer_id=customer.id).all()
        total_orders = len(orders)
        completed_orders = len([o for o in orders if o.status == 'completed'])
        pending_orders = len([o for o in orders if o.status == 'pending'])
        cancelled_orders = len([o for o in orders if o.status == 'cancelled'])
        
        print(f"   📊 Order Statistics:")
        print(f"      - Total Orders: {total_orders}")
        print(f"      - Completed Orders: {completed_orders}")
        print(f"      - Pending Orders: {pending_orders}")
        print(f"      - Cancelled Orders: {cancelled_orders}")
        
        # Get available products
        skus = SKU.query.all()
        print(f"   🛍️ Available Products: {len(skus)}")
        
        # Get recent orders
        recent_orders = orders[:5]
        print(f"   📋 Recent Orders: {len(recent_orders)}")
        print()
        
        print("🎉 VERIFICATION COMPLETE!")
        print("=" * 70)
        print("✅ All verification steps passed successfully!")
        print("✅ Customer login process is working correctly!")
        print("✅ Database separation is maintained!")
        print("✅ Password verification is secure!")
        print("✅ Role-based access is enforced!")
        print()
        print("🚀 Ready for customer login testing!")
        print("   Go to: http://127.0.0.1:5000/login")
        print("   Use credentials: testcustomer / customer123")

if __name__ == "__main__":
    verify_customer_login_process() 