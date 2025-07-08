#!/usr/bin/env python3
"""
PostgreSQL Data Viewer - Multiple Ways to View Your Data
This script provides different methods to view your PostgreSQL data.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import pandas as pd

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def view_all_tables():
    """View all tables and their record counts."""
    print("📋 ALL TABLES OVERVIEW")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"Found {len(tables)} tables in your database:\n")
        
        for table in tables:
            table_name = table['table_name']
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"📊 {table_name}: {count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def view_table_data(table_name, limit=10):
    """View data from a specific table."""
    print(f"\n📋 TABLE: {table_name.upper()}")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get table structure
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' 
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("📋 Table Structure:")
        for col in columns:
            print(f"  - {col['column_name']} ({col['data_type']})")
        
        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_count = cursor.fetchone()['count']
        print(f"\n📊 Total Records: {total_count}")
        
        if total_count > 0:
            # Get sample data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            rows = cursor.fetchall()
            
            print(f"\n📋 Sample Data (showing {len(rows)} records):")
            print("-" * 80)
            
            for i, row in enumerate(rows, 1):
                print(f"Record {i}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing table {table_name}: {e}")

def view_users():
    """View all users in the system."""
    print("\n👥 USERS")
    print("=" * 30)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT username, email, role FROM \"user\" ORDER BY username")
        users = cursor.fetchall()
        
        if users:
            print(f"Found {len(users)} users:\n")
            for user in users:
                print(f"👤 {user['username']}")
                print(f"   Email: {user['email']}")
                print(f"   Role: {user['role']}")
                print()
        else:
            print("No users found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing users: {e}")

def view_customers():
    """View all customers in the system."""
    print("\n👤 CUSTOMERS")
    print("=" * 30)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT username, email FROM customer ORDER BY username")
        customers = cursor.fetchall()
        
        if customers:
            print(f"Found {len(customers)} customers:\n")
            for customer in customers:
                print(f"👤 {customer['username']}")
                print(f"   Email: {customer['email']}")
                print()
        else:
            print("No customers found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing customers: {e}")

def view_skus():
    """View all SKUs in the system."""
    print("\n🏷️  SKUs (Products)")
    print("=" * 30)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT sku_id, name, category, unit_price FROM sku ORDER BY sku_id")
        skus = cursor.fetchall()
        
        if skus:
            print(f"Found {len(skus)} SKUs:\n")
            for sku in skus:
                print(f"🏷️  {sku['sku_id']}")
                print(f"   Name: {sku['name']}")
                print(f"   Category: {sku['category']}")
                print(f"   Price: ₹{sku['unit_price']:.2f}")
                print()
        else:
            print("No SKUs found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing SKUs: {e}")

def view_recent_sales():
    """View recent sales data."""
    print("\n💰 RECENT SALES")
    print("=" * 30)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if amount column exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'sales' 
            AND column_name = 'amount'
        """)
        has_amount = cursor.fetchone() is not None
        
        if has_amount:
            cursor.execute("""
                SELECT s.sku_id, sk.name, s.quantity_sold, s.amount, s.date 
                FROM sales s 
                LEFT JOIN sku sk ON s.sku_id = sk.sku_id 
                ORDER BY s.date DESC 
                LIMIT 10
            """)
        else:
            cursor.execute("""
                SELECT s.sku_id, sk.name, s.quantity_sold, s.date 
                FROM sales s 
                LEFT JOIN sku sk ON s.sku_id = sk.sku_id 
                ORDER BY s.date DESC 
                LIMIT 10
            """)
        
        sales = cursor.fetchall()
        
        if sales:
            print(f"Found {len(sales)} recent sales:\n")
            for sale in sales:
                print(f"💰 {sale['sku_id']} - {sale['name']}")
                print(f"   Quantity: {sale['quantity_sold']}")
                if has_amount:
                    print(f"   Amount: ₹{sale['amount']:.2f}")
                print(f"   Date: {sale['date']}")
                print()
        else:
            print("No sales found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing sales: {e}")

def view_inventory():
    """View current inventory levels."""
    print("\n📦 INVENTORY LEVELS")
    print("=" * 30)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT i.sku_id, sk.name, i.current_level, i.date 
            FROM inventory i 
            LEFT JOIN sku sk ON i.sku_id = sk.sku_id 
            ORDER BY i.date DESC 
            LIMIT 10
        """)
        
        inventory = cursor.fetchall()
        
        if inventory:
            print(f"Found {len(inventory)} inventory records:\n")
            for inv in inventory:
                print(f"📦 {inv['sku_id']} - {inv['name']}")
                print(f"   Current Level: {inv['current_level']:.2f}")
                print(f"   Date: {inv['date']}")
                print()
        else:
            print("No inventory records found in the database.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing inventory: {e}")

def export_to_csv(table_name):
    """Export table data to CSV file."""
    print(f"\n📄 EXPORTING {table_name.upper()} TO CSV")
    print("=" * 50)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in .env file")
            return
        
        # Use pandas to read and export
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", database_url)
        
        filename = f"{table_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Exported {len(df)} records to {filename}")
        print(f"📊 Columns: {', '.join(df.columns.tolist())}")
        
    except Exception as e:
        print(f"❌ Error exporting {table_name}: {e}")

def main():
    """Main function with menu."""
    print("🗄️  PostgreSQL Data Viewer")
    print("=" * 50)
    print("Choose an option:")
    print("1. View all tables overview")
    print("2. View users")
    print("3. View customers")
    print("4. View SKUs (products)")
    print("5. View recent sales")
    print("6. View inventory levels")
    print("7. View specific table data")
    print("8. Export table to CSV")
    print("9. View everything")
    print("0. Exit")
    
    while True:
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            view_all_tables()
        elif choice == '2':
            view_users()
        elif choice == '3':
            view_customers()
        elif choice == '4':
            view_skus()
        elif choice == '5':
            view_recent_sales()
        elif choice == '6':
            view_inventory()
        elif choice == '7':
            table_name = input("Enter table name: ").strip()
            limit = input("Enter number of records to show (default 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            view_table_data(table_name, limit)
        elif choice == '8':
            table_name = input("Enter table name to export: ").strip()
            export_to_csv(table_name)
        elif choice == '9':
            view_all_tables()
            view_users()
            view_customers()
            view_skus()
            view_recent_sales()
            view_inventory()
        else:
            print("❌ Invalid choice. Please enter 0-9.")

if __name__ == '__main__':
    main() 