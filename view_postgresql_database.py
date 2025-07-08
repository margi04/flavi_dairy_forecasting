#!/usr/bin/env python3
"""
PostgreSQL Database Viewer Script for Flavi Dairy Forecasting AI
This script allows you to view the contents of your PostgreSQL database.
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def view_postgresql_database():
    """View the PostgreSQL database contents."""
    print("🗄️  PostgreSQL Database Viewer")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        print("Please make sure you have set up PostgreSQL and created a .env file")
        return
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get database info
        cursor.execute("SELECT current_database(), current_user, version()")
        db_info = cursor.fetchone()
        
        print(f"🗄️  Database: {db_info['current_database']}")
        print(f"👤 User: {db_info['current_user']}")
        print(f"🐘 PostgreSQL Version: {db_info['version'].split(',')[0]}")
        print("=" * 60)
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print("📋 Tables in database:")
        for table in tables:
            table_name = table['table_name']
            print(f"  - {table_name}")
            
            # Get row count for each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"    Records: {count}")
            
            # Show sample data for each table
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                sample_data = cursor.fetchall()
                
                # Get column names
                cursor.execute(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}' 
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                
                column_names = [col['column_name'] for col in columns]
                print(f"    Columns: {', '.join(column_names)}")
                print("    Sample data:")
                for row in sample_data:
                    print(f"      {dict(row)}")
            print()
        
        # Show detailed information for specific tables
        print("🔍 Detailed Information:")
        print("-" * 40)
        
        # Users table
        if any(table['table_name'] == 'user' for table in tables):
            print("\n👥 Users:")
            try:
                cursor.execute("SELECT username, email, role FROM \"user\" LIMIT 5")
                users = cursor.fetchall()
                for user in users:
                    print(f"  {user['username']} ({user['email']}) - {user['role']}")
            except Exception as e:
                print(f"  Error reading users: {e}")
        
        # Customers table
        if any(table['table_name'] == 'customer' for table in tables):
            print("\n👤 Customers:")
            try:
                cursor.execute("SELECT username, email FROM customer LIMIT 5")
                customers = cursor.fetchall()
                for customer in customers:
                    print(f"  {customer['username']} ({customer['email']})")
            except Exception as e:
                print(f"  Error reading customers: {e}")
        
        # SKUs table
        if any(table['table_name'] == 'sku' for table in tables):
            print("\n🏷️  SKUs:")
            try:
                cursor.execute("SELECT sku_id, name, category FROM sku LIMIT 5")
                skus = cursor.fetchall()
                for sku in skus:
                    print(f"  {sku['sku_id']} - {sku['name']} ({sku['category']})")
            except Exception as e:
                print(f"  Error reading SKUs: {e}")
        
        # Sales table
        if any(table['table_name'] == 'sales' for table in tables):
            print("\n💰 Recent Sales:")
            try:
                # First check what columns exist in sales table
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'sales' 
                    ORDER BY ordinal_position
                """)
                sales_columns = [col['column_name'] for col in cursor.fetchall()]
                print(f"  Sales table columns: {sales_columns}")
                
                if 'amount' in sales_columns:
                    cursor.execute("""
                        SELECT sku_id, quantity_sold, amount, date 
                        FROM sales 
                        ORDER BY date DESC 
                        LIMIT 5
                    """)
                else:
                    cursor.execute("""
                        SELECT sku_id, quantity_sold, date 
                        FROM sales 
                        ORDER BY date DESC 
                        LIMIT 5
                    """)
                
                sales = cursor.fetchall()
                for sale in sales:
                    if 'amount' in sale:
                        print(f"  {sale['sku_id']} - Qty: {sale['quantity_sold']}, Amount: ₹{sale['amount']:.2f}, Date: {sale['date']}")
                    else:
                        print(f"  {sale['sku_id']} - Qty: {sale['quantity_sold']}, Date: {sale['date']}")
            except Exception as e:
                print(f"  Error reading sales: {e}")
        
        # Inventory table
        if any(table['table_name'] == 'inventory' for table in tables):
            print("\n📦 Recent Inventory:")
            try:
                cursor.execute("""
                    SELECT sku_id, current_level, date 
                    FROM inventory 
                    ORDER BY date DESC 
                    LIMIT 5
                """)
                inventory = cursor.fetchall()
                for inv in inventory:
                    print(f"  {inv['sku_id']} - Level: {inv['current_level']:.2f}, Date: {inv['date']}")
            except Exception as e:
                print(f"  Error reading inventory: {e}")
        
        # Show database statistics
        print("\n📊 Database Statistics:")
        print("-" * 30)
        
        total_tables = len(tables)
        total_records = 0
        
        for table in tables:
            table_name = table['table_name']
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()['count']
            total_records += count
            print(f"  {table_name}: {count} records")
        
        print(f"\n📈 Summary:")
        print(f"  Total tables: {total_tables}")
        print(f"  Total records: {total_records}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading PostgreSQL database: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your .env file has the correct DATABASE_URL")
        print("3. Verify the database and user exist")
        print("4. Ensure the user has proper permissions")

if __name__ == '__main__':
    view_postgresql_database() 