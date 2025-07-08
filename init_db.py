#!/usr/bin/env python3
"""
Database Initialization Script for Flavi Dairy Forecasting AI
This script creates all database tables and populates them with sample data.
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from app.models.sku import SKU
from app.models.sales import Sales
from app.models.inventory import Inventory

def init_database():
    """Initialize the database with all tables and sample data."""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Initializing database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if data already exists
        if User.query.first() or Customer.query.first() or SKU.query.first():
            print("⚠️  Database already contains data. Skipping sample data creation.")
            return
        
        print("📊 Adding sample data...")
        
        # Create sample admin users
        admin_users = [
            {
                'username': 'admin',
                'email': 'admin@flavidairy.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'manager',
                'email': 'manager@flavidairy.com',
                'password': 'manager123',
                'role': 'admin'
            }
        ]
        
        for admin_data in admin_users:
            admin = User(
                username=admin_data['username'],
                email=admin_data['email'],
                role=admin_data['role']
            )
            admin.set_password(admin_data['password'])
            db.session.add(admin)
        
        print("👥 Admin users created")
        
        # Create sample customers
        customers = [
            {
                'username': 'customer1',
                'email': 'customer1@example.com',
                'password': 'customer123'
            },
            {
                'username': 'customer2',
                'email': 'customer2@example.com',
                'password': 'customer123'
            },
            {
                'username': 'customer3',
                'email': 'customer3@example.com',
                'password': 'customer123'
            },
            {
                'username': 'customer4',
                'email': 'customer4@example.com',
                'password': 'customer123'
            },
            {
                'username': 'customer5',
                'email': 'customer5@example.com',
                'password': 'customer123'
            }
        ]
        
        for customer_data in customers:
            customer = Customer(
                username=customer_data['username'],
                email=customer_data['email']
            )
            customer.set_password(customer_data['password'])
            db.session.add(customer)
        
        print("👤 Customers created")
        
        # Create sample SKUs
        skus = [
            {
                'sku_id': 'MILK-001',
                'name': 'Full Cream Milk 1L',
                'category': 'Milk',
                'packaging_type': 'Plastic Bottle',
                'unit_of_measure': 'Liters',
                'processing_time_hours': 2.5,
                'packaging_time_hours': 1.0,
                'storage_requirement_cubic_meters': 0.001,
                'min_threshold': 100
            },
            {
                'sku_id': 'MILK-002',
                'name': 'Toned Milk 1L',
                'category': 'Milk',
                'packaging_type': 'Plastic Bottle',
                'unit_of_measure': 'Liters',
                'processing_time_hours': 2.0,
                'packaging_time_hours': 1.0,
                'storage_requirement_cubic_meters': 0.001,
                'min_threshold': 80
            },
            {
                'sku_id': 'CURD-001',
                'name': 'Fresh Curd 500g',
                'category': 'Curd',
                'packaging_type': 'Plastic Container',
                'unit_of_measure': 'Grams',
                'processing_time_hours': 4.0,
                'packaging_time_hours': 1.5,
                'storage_requirement_cubic_meters': 0.0005,
                'min_threshold': 50
            },
            {
                'sku_id': 'BUTTER-001',
                'name': 'Unsalted Butter 250g',
                'category': 'Butter',
                'packaging_type': 'Paper Wrapper',
                'unit_of_measure': 'Grams',
                'processing_time_hours': 6.0,
                'packaging_time_hours': 2.0,
                'storage_requirement_cubic_meters': 0.0003,
                'min_threshold': 30
            },
            {
                'sku_id': 'CHEESE-001',
                'name': 'Cheddar Cheese 200g',
                'category': 'Cheese',
                'packaging_type': 'Vacuum Pack',
                'unit_of_measure': 'Grams',
                'processing_time_hours': 8.0,
                'packaging_time_hours': 2.5,
                'storage_requirement_cubic_meters': 0.0002,
                'min_threshold': 25
            },
            {
                'sku_id': 'GHEE-001',
                'name': 'Pure Ghee 1L',
                'category': 'Ghee',
                'packaging_type': 'Glass Jar',
                'unit_of_measure': 'Liters',
                'processing_time_hours': 12.0,
                'packaging_time_hours': 3.0,
                'storage_requirement_cubic_meters': 0.001,
                'min_threshold': 20
            }
        ]
        
        for sku_data in skus:
            sku = SKU(**sku_data)
            db.session.add(sku)
        
        print("🏷️  SKUs created")
        
        # Commit all the basic data first
        db.session.commit()
        
        # Create sample inventory records
        print("📦 Creating inventory records...")
        for sku in SKU.query.all():
            # Create inventory records for the last 30 days
            for i in range(30):
                date = datetime.now().date() - timedelta(days=i)
                
                # Generate realistic inventory levels
                base_level = random.uniform(50, 200)
                current_level = max(0, base_level + random.uniform(-20, 20))
                
                inventory = Inventory(
                    sku_id=sku.sku_id,
                    current_level=current_level,
                    production_batch_size=random.uniform(100, 500),
                    shelf_life_days=random.randint(7, 30),
                    storage_capacity_units=random.uniform(500, 1000),
                    date=date
                )
                db.session.add(inventory)
        
        # Create sample sales records
        print("💰 Creating sales records...")
        customers = Customer.query.all()
        skus = SKU.query.all()
        
        # Create sales for the last 90 days
        for i in range(90):
            date = datetime.now().date() - timedelta(days=i)
            
            # Generate 1-5 sales per day
            daily_sales = random.randint(1, 5)
            for _ in range(daily_sales):
                sku = random.choice(skus)
                customer = random.choice(customers)
                
                # Generate realistic sales quantities
                quantity = random.randint(1, 10)
                unit_price = random.uniform(20, 200)  # Price in rupees
                amount = quantity * unit_price
                
                sale = Sales(
                    sku_id=sku.sku_id,
                    customer_id=customer.id,
                    quantity_sold=quantity,
                    amount=amount,
                    date=date
                )
                db.session.add(sale)
        
        # Commit all data
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📋 Database Summary:")
        print(f"   👥 Admin Users: {User.query.filter_by(role='admin').count()}")
        print(f"   👤 Customers: {Customer.query.count()}")
        print(f"   🏷️  SKUs: {SKU.query.count()}")
        print(f"   📦 Inventory Records: {Inventory.query.count()}")
        print(f"   💰 Sales Records: {Sales.query.count()}")
        
        print("\n🔑 Default Login Credentials:")
        print("   Admin: admin / admin123")
        print("   Manager: manager / manager123")
        print("   Customer: customer1 / customer123")
        
        print("\n🚀 Database initialization completed successfully!")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        sys.exit(1)
