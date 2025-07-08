#!/usr/bin/env python3
"""
Database Setup Script for Flavi Dairy Forecasting AI
This script handles database initialization, migrations, and data seeding.
"""

import os
import sys
import argparse
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from app.models.sku import SKU
from app.models.sales import Sales
from app.models.inventory import Inventory

def setup_database(force=False, seed_data=True):
    """Set up the database with tables and optional sample data."""
    app = create_app()
    
    with app.app_context():
        print("🚀 Setting up Flavi Dairy Forecasting AI Database")
        print("=" * 60)
        
        try:
            # Create tables
            print("\n📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if data already exists
            if not force and (User.query.first() or Customer.query.first() or SKU.query.first()):
                print("⚠️  Database already contains data.")
                if seed_data:
                    response = input("Do you want to add sample data anyway? (y/N): ")
                    if response.lower() != 'y':
                        print("Skipping sample data creation.")
                        return
                else:
                    print("Skipping sample data creation.")
                    return
            
            if seed_data:
                print("\n🌱 Adding sample data...")
                add_sample_data()
            
            print("\n✅ Database setup completed successfully!")
            print_sample_credentials()
            
        except Exception as e:
            print(f"❌ Error setting up database: {str(e)}")
            sys.exit(1)

def add_sample_data():
    """Add sample data to the database."""
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
        if not User.query.filter_by(username=admin_data['username']).first():
            admin = User(
                username=admin_data['username'],
                email=admin_data['email'],
                role=admin_data['role']
            )
            admin.set_password(admin_data['password'])
            db.session.add(admin)
    
    print("👥 Admin users created")
    
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
        if not SKU.query.filter_by(sku_id=sku_data['sku_id']).first():
            sku = SKU(**sku_data)
            db.session.add(sku)
    
    print("🏷️  SKUs created")
    
    # Commit all the basic data first
    db.session.commit()
    
    # Create sample inventory and sales records only if there are customers
    if Customer.query.count() > 0:
        print("📦 Creating inventory and sales records...")
        add_sample_inventory_and_sales()
        print("✅ Sample data added successfully!")
    else:
        print("⚠️  No customers found. Skipping inventory and sales sample data.")

def add_sample_inventory_and_sales():
    """Add sample inventory and sales records."""
    import random
    from datetime import timedelta
    
    # Create inventory records for the last 30 days
    for sku in SKU.query.all():
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
    
    # Create sales records for the last 90 days
    customers = Customer.query.all()
    skus = SKU.query.all()
    
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
    
    db.session.commit()

def print_sample_credentials():
    """Print sample login credentials."""
    print("\n🔑 Sample Login Credentials:")
    print("-" * 40)
    print("Admin Users:")
    print("  Username: admin, Password: admin123")
    print("  Username: manager, Password: manager123")
    print("\nCustomer Users:")
    print("  Username: customer1, Password: customer123")
    print("  Username: customer2, Password: customer123")
    print("  Username: customer3, Password: customer123")
    print("  Username: customer4, Password: customer123")
    print("  Username: customer5, Password: customer123")

def reset_database():
    """Reset the database (drop all tables and recreate)."""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Resetting database...")
        
        try:
            db.drop_all()
            print("✅ All tables dropped")
            
            db.create_all()
            print("✅ Tables recreated")
            
            print("\n🌱 Adding sample data...")
            add_sample_data()
            
            print("\n✅ Database reset completed!")
            print_sample_credentials()
            
        except Exception as e:
            print(f"❌ Error resetting database: {str(e)}")
            sys.exit(1)

def show_database_info():
    """Show database information."""
    app = create_app()
    
    with app.app_context():
        print("🔍 Database Information")
        print("=" * 40)
        
        # Get connection info from existing database instance
        try:
            engine = db.engine
            url = engine.url
            
            info = {
                'database_type': url.drivername,
                'host': getattr(url, 'host', 'N/A'),
                'port': getattr(url, 'port', 'N/A'),
                'database': getattr(url, 'database', 'N/A'),
                'username': getattr(url, 'username', 'N/A'),
            }
            
            print(f"Database Type: {info['database_type']}")
            print(f"Host: {info['host']}")
            print(f"Port: {info['port']}")
            print(f"Database: {info['database']}")
            print(f"Username: {info['username']}")
            
        except Exception as e:
            print(f"❌ Error getting connection info: {str(e)}")
        
        # Show table counts
        print(f"\n📊 Data Summary:")
        print(f"  Admin Users: {User.query.filter_by(role='admin').count()}")
        print(f"  Customers: {Customer.query.count()}")
        print(f"  SKUs: {SKU.query.count()}")
        print(f"  Inventory Records: {Inventory.query.count()}")
        print(f"  Sales Records: {Sales.query.count()}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Flavi Dairy Forecasting AI Database Setup')
    parser.add_argument('--force', action='store_true', help='Force setup even if data exists')
    parser.add_argument('--no-seed', action='store_true', help='Skip adding sample data')
    parser.add_argument('--reset', action='store_true', help='Reset database (drop all tables)')
    parser.add_argument('--info', action='store_true', help='Show database information')
    
    args = parser.parse_args()
    
    if args.info:
        show_database_info()
    elif args.reset:
        reset_database()
    else:
        setup_database(force=args.force, seed_data=not args.no_seed)

if __name__ == '__main__':
    main() 